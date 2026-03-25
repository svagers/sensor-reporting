from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Sensor, SensorType, Metric, Unit, MetricUnit, Measurement
from django.utils import timezone


class MeasurementsViewTest(TestCase):
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
        
        self.unit = Unit.objects.create(
            id=1,
            name='Celsius',
            precision=2
        )
        
        MetricUnit.objects.create(
            metric=self.metric,
            unit=self.unit,
            is_primary=True
        )
        
        Measurement.objects.create(
            sensor=self.sensor,
            metric=self.metric,
            unit=self.unit,
            value=25.5,
            measured_at=timezone.now()
        )
    
    def test_measurements_list_success(self):
        response = self.client.post('/api/measurements', {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('page', response.data)
        self.assertIn('per_page', response.data)
        self.assertIn('total', response.data)
        self.assertIn('total_pages', response.data)
    
    def test_measurements_list_with_pagination(self):
        response = self.client.post('/api/measurements', {
            'page': 1,
            'limit': 10
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['per_page'], 10)
    
    def test_measurements_list_with_sensor_name_filter(self):
        response = self.client.post('/api/measurements', {
            'sensor_name': 'es'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['total'], 0)
    
    def test_measurements_list_with_type_id_filter(self):
        response = self.client.post('/api/measurements', {
            'type_id': 1
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_measurements_list_with_variant_id_filter(self):
        response = self.client.post('/api/measurements', {
            'type_id': 1,
            'variant_id': 1
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_measurements_list_variant_id_without_type_id_fails(self):
        response = self.client.post('/api/measurements', {
            'variant_id': 1
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('variant_id', response.data)
    
    def test_measurements_list_invalid_page(self):
        response = self.client.post('/api/measurements', {
            'page': 0
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_measurements_list_invalid_order(self):
        response = self.client.post('/api/measurements', {
            'order': 'invalid'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
