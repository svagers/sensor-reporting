"""
Sensors API tests: seed data via the same bulk_upsert paths as import commands, then assert response integrity.
"""

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from api.factories import MeasurementFactory, MetricFactory, SensorFactory
from api.models import Metric, Sensor, SensorType
from api.repositories import MeasurementRepository, MetricRepository, SensorRepository


class SensorsViewTest(TestCase):
    """GET /api/sensors — reporter-backed list with metric columns."""

    def setUp(self):
        self.client = APIClient()
        self.sensor_repo = SensorRepository()
        self.metric_repo = MetricRepository()
        self.measurement_repo = MeasurementRepository()
        self._sensor_factory = SensorFactory()
        self._metric_factory = MetricFactory()
        self._measurement_factory = MeasurementFactory()

        self._seed_sensor_types()
        self._seed_metrics_with_units()
        self._seed_sensors()
        self._seed_measurements()

    def _seed_sensor_types(self):
        types_ = [
            SensorType(type_id=1, variant_id=1, name="Temperature probe"),
            SensorType(type_id=1, variant_id=2, name="Temperature probe (outdoor)"),
            SensorType(type_id=2, variant_id=1, name="Humidity sensor"),
        ]
        self.assertEqual(self.sensor_repo.bulk_upsert_sensor_types(types_), 3)
        self.st_temp_indoor = SensorType.objects.get(type_id=1, variant_id=1)
        self.st_temp_outdoor = SensorType.objects.get(type_id=1, variant_id=2)
        self.st_humidity = SensorType.objects.get(type_id=2, variant_id=1)

    def _seed_metrics_with_units(self):
        # Measured metrics (101–103) + unused metrics (201–202) with no measurements
        metrics = [
            Metric(id=101, name="Temperature"),
            Metric(id=102, name="Humidity"),
            Metric(id=103, name="CO2"),
            Metric(id=201, name="Pressure"),
            Metric(id=202, name="Battery voltage"),
        ]
        self.assertEqual(self.metric_repo.bulk_upsert_metrics(metrics), 5)

        units = [
            self._metric_factory.create_unit(1001, "°C", 1),
            self._metric_factory.create_unit(1002, "%", 0),
            self._metric_factory.create_unit(1003, "ppm", 0),
            self._metric_factory.create_unit(1004, "K", 2),
            self._metric_factory.create_unit(1005, "g/m³", 2),
            self._metric_factory.create_unit(1006, "ppb", 0),
            self._metric_factory.create_unit(2001, "hPa", 0),
            self._metric_factory.create_unit(2002, "V", 2),
        ]
        self.assertEqual(self.metric_repo.bulk_upsert_units(units), 8)

        metric_units = [
            # Primary + secondary (non-primary) for measured metrics
            self._metric_factory.create_metric_unit(101, 1001, True),
            self._metric_factory.create_metric_unit(101, 1004, False),
            self._metric_factory.create_metric_unit(102, 1002, True),
            self._metric_factory.create_metric_unit(102, 1005, False),
            self._metric_factory.create_metric_unit(103, 1003, True),
            self._metric_factory.create_metric_unit(103, 1006, False),
            # Unused metrics still have units in DB (never referenced by measurements)
            self._metric_factory.create_metric_unit(201, 2001, True),
            self._metric_factory.create_metric_unit(202, 2002, True),
        ]
        self.assertEqual(self.metric_repo.bulk_upsert_metric_units(metric_units), 8)

    def _seed_sensors(self):
        sensors = [
            self._sensor_factory.create_sensor(5001, "Lab sensor A", self.st_temp_indoor),
            self._sensor_factory.create_sensor(5002, "Lab sensor B", self.st_temp_indoor),
            self._sensor_factory.create_sensor(5003, "Roof sensor", self.st_temp_outdoor),
            self._sensor_factory.create_sensor(5004, "Storage humidity", self.st_humidity),
            # Null name, type attached
            self._sensor_factory.create_sensor(5005, None, self.st_temp_indoor),
            # Named, no sensor type
            self._sensor_factory.create_sensor(5006, "Orphan hardware id", None),
            # Null name and null type
            self._sensor_factory.create_sensor(5007, None, None),
        ]
        self.assertEqual(self.sensor_repo.bulk_upsert(sensors), 7)

    def _seed_measurements(self):
        t0 = timezone.now()
        s = {sid: Sensor.objects.get(pk=sid) for sid in range(5001, 5008)}
        m = {mid: Metric.objects.get(pk=mid) for mid in (101, 102, 103)}

        measurements = [
            self._measurement_factory.create_measurement(s[5001], m[101], 22.4, t0),
            self._measurement_factory.create_measurement(s[5001], m[102], 48.0, t0),
            self._measurement_factory.create_measurement(s[5002], m[101], 23.1, t0),
            self._measurement_factory.create_measurement(s[5002], m[103], 412.0, t0),
            self._measurement_factory.create_measurement(s[5003], m[101], 19.8, t0),
            self._measurement_factory.create_measurement(s[5004], m[102], 62.5, t0),
            self._measurement_factory.create_measurement(s[5005], m[101], 21.0, t0),
            self._measurement_factory.create_measurement(s[5006], m[102], 55.0, t0),
        ]
        self.assertEqual(self.measurement_repo.bulk_upsert(measurements), 8)

    def test_sensors_list_success(self):
        response = self.client.get("/api/sensors")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIsInstance(response.data["data"], list)
        self.assertEqual(len(response.data["data"]), 7)

    def test_sensors_response_columns_and_types(self):
        response = self.client.get("/api/sensors")
        rows = response.data["data"]

        # Reporter only adds columns for metrics that appear in measurements (not 201/202)
        used_metric_ids = {101, 102, 103}
        unused_metric_ids = {201, 202}

        for row in rows:
            self.assertIn("id", row)
            self.assertIn("name", row)
            self.assertIn("type_id", row)
            for mid in used_metric_ids:
                self.assertIn(f"metric_{mid}", row)
            for mid in unused_metric_ids:
                self.assertNotIn(f"metric_{mid}", row)

    def test_sensors_data_integrity(self):
        response = self.client.get("/api/sensors")
        rows = {row["id"]: row for row in response.data["data"]}

        self.assertEqual(rows[5001]["name"], "Lab sensor A")
        self.assertEqual(rows[5001]["type_id"], self.st_temp_indoor.id)
        self.assertAlmostEqual(rows[5001]["metric_101"], 22.4)
        self.assertAlmostEqual(rows[5001]["metric_102"], 48.0)
        self.assertIsNone(rows[5001].get("metric_103"))

        self.assertEqual(rows[5002]["name"], "Lab sensor B")
        self.assertAlmostEqual(rows[5002]["metric_101"], 23.1)
        self.assertAlmostEqual(rows[5002]["metric_103"], 412.0)

        self.assertEqual(rows[5003]["name"], "Roof sensor")
        self.assertEqual(rows[5003]["type_id"], self.st_temp_outdoor.id)
        self.assertAlmostEqual(rows[5003]["metric_101"], 19.8)

        self.assertEqual(rows[5004]["name"], "Storage humidity")
        self.assertEqual(rows[5004]["type_id"], self.st_humidity.id)
        self.assertAlmostEqual(rows[5004]["metric_102"], 62.5)

        self.assertIsNone(rows[5005]["name"])
        self.assertEqual(rows[5005]["type_id"], self.st_temp_indoor.id)
        self.assertAlmostEqual(rows[5005]["metric_101"], 21.0)

        self.assertEqual(rows[5006]["name"], "Orphan hardware id")
        self.assertIsNone(rows[5006]["type_id"])
        self.assertAlmostEqual(rows[5006]["metric_102"], 55.0)

        self.assertIsNone(rows[5007]["name"])
        self.assertIsNone(rows[5007]["type_id"])
        self.assertIsNone(rows[5007].get("metric_101"))
        self.assertIsNone(rows[5007].get("metric_102"))
        self.assertIsNone(rows[5007].get("metric_103"))
