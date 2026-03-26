"""
Validate django/data JSON fixtures without touching the database.

sensors.json nests measurements under each sensor id. This module ensures no
measurement references a sensor id that is not present in the fixture.
"""

import json
import os
from typing import Any, List, Set, Tuple

from django.conf import settings
from django.test import SimpleTestCase


def _data_dir() -> str:
    return os.path.join(settings.BASE_DIR, "data")


def _load_json(filename: str) -> dict:
    path = os.path.join(_data_dir(), filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _sensor_id_keys(root: dict) -> Set[str]:
    """Top-level keys that identify a sensor (numeric string ids in current schema)."""
    return {k for k in root if str(k).isdigit()}


def _normalize_sensor_ref(val: Any) -> str:
    """Normalize a sensor id from JSON (int or string) to a string comparable to top-level keys."""
    if isinstance(val, bool):
        return str(val)
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float) and val == int(val):
        return str(int(val))
    s = str(val).strip()
    if s.isdigit():
        return str(int(s))
    return s


def _explicit_sensor_refs_in_measurement(measurement: dict) -> List[Tuple[str, Any]]:
    """Optional fields that explicitly name another sensor (future-proof)."""
    refs: List[Tuple[str, Any]] = []
    for key in ("sensor_id", "sensorId", "sensor"):
        if key not in measurement:
            continue
        val = measurement[key]
        if isinstance(val, dict):
            continue
        refs.append((key, val))
    return refs


def _violations_for_nested_metrics(
    sensors_root: dict, known_sensor_ids: Set[str]
) -> List[str]:
    bad: List[str] = []
    for sensor_key, sensor in sensors_root.items():
        if not str(sensor_key).isdigit():
            continue
        if sensor_key not in known_sensor_ids:
            bad.append(f"inconsistent: sensor key {sensor_key!r} not in known set")
            continue
        metrics = sensor.get("metrics") or {}
        for metric_key, measurement in metrics.items():
            if not isinstance(measurement, dict):
                continue
            for ref_key, ref_val in _explicit_sensor_refs_in_measurement(measurement):
                ref_id = _normalize_sensor_ref(ref_val)
                if ref_id not in known_sensor_ids:
                    bad.append(
                        f"sensor {sensor_key} metric {metric_key}: "
                        f"{ref_key}={ref_val!r} points to unknown sensor {ref_id!r}"
                    )
    return bad


def _violations_for_flat_measurements(
    sensors_root: dict, known_sensor_ids: Set[str]
) -> List[str]:
    """If root has a `measurements` array, each row must reference an existing sensor."""
    bad: List[str] = []
    flat = sensors_root.get("measurements")
    if not isinstance(flat, list):
        return bad
    for i, item in enumerate(flat):
        if not isinstance(item, dict):
            continue
        sid = item.get("sensor_id") or item.get("sensorId") or item.get("sensor")
        if sid is None or isinstance(sid, dict):
            continue
        ref_id = _normalize_sensor_ref(sid)
        if ref_id not in known_sensor_ids:
            bad.append(
                f"measurements[{i}]: references unknown sensor {ref_id!r} (raw={sid!r})"
            )
    return bad


class SensorsJsonMeasurementReferencesTest(SimpleTestCase):
    """Measurements must not reference sensor ids missing from sensors.json."""

    def test_no_measurement_references_unknown_sensor(self):
        root = _load_json("sensors.json")
        self.assertIsInstance(root, dict)

        known = _sensor_id_keys(root)
        self.assertGreater(len(known), 0, "sensors.json must list at least one sensor id")

        nested = _violations_for_nested_metrics(root, known)
        flat = _violations_for_flat_measurements(root, known)
        all_bad = nested + flat

        self.assertEqual(
            all_bad,
            [],
            "Measurements reference sensor ids that are not present in sensors.json:\n"
            + "\n".join(all_bad),
        )
