"""
Integration tests: run import management commands against django/data JSON fixtures,
then assert /api/structure and /api/sensors match those fixtures.

Structure lists only sensor types and metrics that are actually used (see repositories).
Some sensors reference (type, variant) pairs missing from sensorTypes.json; those rows
keep a null sensor_type FK and are omitted from structure's sensor_types list.
"""

import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Sensor


# --- Loading fixtures ---


def _fixture_path(filename: str) -> str:
    return os.path.join(settings.BASE_DIR, "data", filename)


def _load_fixture(filename: str) -> dict:
    with open(_fixture_path(filename), encoding="utf-8") as f:
        return json.load(f)


def _normalize_sensor_name(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    s = str(raw).strip()
    return None if s == "" else s


# --- Deriving expectations from sensors.json + metrics.json ---


def _metric_ids_referenced_by_sensors(sensors_data: dict) -> Set[int]:
    ids: Set[int] = set()
    for sensor in sensors_data.values():
        for metric_key in sensor.get("metrics") or {}:
            ids.add(int(metric_key))
    return ids


def _metrics_by_id(metrics_json: dict) -> Dict[int, dict]:
    return {int(item["id"]): item for item in metrics_json["data"]["items"]}


def _primary_unit_dict(metric_item: dict) -> dict:
    units = metric_item.get("units") or []
    primary = next((u for u in units if u.get("selected")), None)
    if primary is None and units:
        primary = units[0]
    assert primary is not None, f"no unit for metric {metric_item.get('id')}"
    return {
        "id": int(primary["id"]),
        "name": primary["name"],
        "precision": int(primary["precision"]),
    }


def _expected_metrics_for_structure(
    metrics_json: dict, used_metric_ids: Set[int]
) -> List[dict]:
    by_id = _metrics_by_id(metrics_json)
    return [
        {
            "id": mid,
            "name": by_id[mid]["name"],
            "primary_unit": _primary_unit_dict(by_id[mid]),
        }
        for mid in sorted(used_metric_ids)
    ]


def _type_variant_pairs_defined_in_fixtures(
    sensor_types_json: dict, sensors_data: dict
) -> Set[Tuple[int, int]]:
    """
    (type_id, variant_id) pairs that appear on at least one sensor and exist in
    sensorTypes.json. Pairs missing from sensorTypes.json are skipped by import
    (sensor gets null sensor_type) and do not appear in /api/structure.
    """
    pairs: Set[Tuple[int, int]] = set()
    for sensor in sensors_data.values():
        t, v = int(sensor["type"]), int(sensor["variant"])
        ts, vs = str(t), str(v)
        if ts in sensor_types_json and vs in sensor_types_json[ts]:
            pairs.add((t, v))
    return pairs


def _sensor_type_display_name_by_pair(sensor_types_json: dict) -> Dict[Tuple[int, int], str]:
    return {
        (int(tid), int(vid)): variant["name"]
        for tid, variants in sensor_types_json.items()
        for vid, variant in variants.items()
    }


class ImportCommandsApiIntegrationTest(TestCase):
    """Seeds DB via import_sensor_types → import_metrics → import_sensors."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sensor_types_fixture = _load_fixture("sensorTypes.json")
        cls.metrics_fixture = _load_fixture("metrics.json")
        cls.sensors_fixture = _load_fixture("sensors.json")

    def setUp(self):
        self.client = APIClient()
        call_command("import_sensor_types", verbosity=0)
        call_command("import_metrics", verbosity=0)
        call_command("import_sensors", verbosity=0)

    def test_structure_endpoint_matches_json(self):
        """GET /api/structure matches fixture names for used types and metrics."""
        response = self.client.get("/api/structure")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pairs_in_structure = _type_variant_pairs_defined_in_fixtures(
            self.sensor_types_fixture, self.sensors_fixture
        )
        names_by_pair = _sensor_type_display_name_by_pair(self.sensor_types_fixture)

        api_types = sorted(
            response.data["sensor_types"],
            key=lambda x: (x["type_id"], x["variant_id"]),
        )
        self.assertEqual(len(api_types), len(pairs_in_structure))
        for st in api_types:
            pair = (st["type_id"], st["variant_id"])
            with self.subTest(pair=pair):
                self.assertIn(pair, pairs_in_structure)
                self.assertEqual(st["name"], names_by_pair[pair])

        used_metric_ids = _metric_ids_referenced_by_sensors(self.sensors_fixture)
        expected_metrics = _expected_metrics_for_structure(
            self.metrics_fixture, used_metric_ids
        )
        api_metrics = sorted(response.data["metrics"], key=lambda x: x["id"])
        self.assertEqual(api_metrics, expected_metrics)

    def test_sensors_endpoint_matches_json(self):
        """GET /api/sensors: one row per fixture sensor; values match sensors.json."""
        response = self.client.get("/api/sensors")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        by_id = {row["id"]: row for row in response.data["data"]}
        self.assertEqual(len(by_id), len(self.sensors_fixture))

        used_metric_ids = _metric_ids_referenced_by_sensors(self.sensors_fixture)

        for sid_str, sensor_json in self.sensors_fixture.items():
            sid = int(sid_str)
            with self.subTest(sensor_id=sid):
                self.assertIn(sid, by_id)
                row = by_id[sid]

                self.assertEqual(
                    row["name"],
                    _normalize_sensor_name(sensor_json.get("name")),
                )

                db_sensor = Sensor.objects.get(pk=sid)
                if db_sensor.sensor_type_id is None:
                    self.assertIsNone(row.get("type_id"))
                else:
                    self.assertEqual(row["type_id"], db_sensor.sensor_type_id)

                metrics_in_file = sensor_json.get("metrics") or {}
                for mid in used_metric_ids:
                    column = f"metric_{mid}"
                    self.assertIn(column, row)
                    if str(mid) in metrics_in_file:
                        expected = float(metrics_in_file[str(mid)]["v"])
                        self.assertIsNotNone(row[column])
                        self.assertAlmostEqual(float(row[column]), expected, places=6)
                    else:
                        self.assertIsNone(row[column])
