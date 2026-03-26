from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Sensor, SensorType, Metric, Measurement
from django.utils import timezone


class SensorsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.sensor_type = SensorType.objects.create(
            type_id=1,
            variant_id=1,
            name='Temperature Sensor'
        )

        self.sensor = Sensor.objects.create(
            id=1,
            name='Test Sensor',
            sensor_type=self.sensor_type
        )

        self.metric = Metric.objects.create(
            id=1,
            name='Temperature'
        )

        Measurement.objects.create(
            sensor=self.sensor,
            metric=self.metric,
            value=25.5,
            measured_at=timezone.now()
        )

    def test_sensors_list_success(self):
        response = self.client.get('/api/sensors')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsInstance(response.data['data'], list)
        self.assertGreaterEqual(len(response.data['data']), 1)
