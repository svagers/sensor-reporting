from datetime import datetime
from django.core.management.base import CommandError
from django.utils import timezone
from api.repositories import SensorRepository, MeasurementRepository
from api.factories import SensorFactory, MeasurementFactory
from api.serializers.sensor_import_serializers import SensorSerializer, MeasurementSerializer
from .base_import_command import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import sensors and measurements data from JSON file'

    def __init__(self):
        super().__init__()
        self._sensor_repo = SensorRepository()
        self._measurement_repo = MeasurementRepository()
        self._sensor_factory = SensorFactory()
        self._measurement_factory = MeasurementFactory()
        self._imported_sensors = []
        self._imported_measurements = []
    
    def get_json_file_name(self) -> str:
        return 'sensors.json'

    def import_data(self, raw_data: dict) -> None:
        for sensor_id, sensor_data in raw_data.items():
            sensor_domain = self.make_sensor(sensor_id, sensor_data)
            
            if sensor_domain is not None:
                self._imported_sensors.append(sensor_domain)
        
        for sensor_domain, metrics_data in self._imported_sensors:
            for metric_id, measurement_data in metrics_data.items():
                measurement_domain = self.make_measurement(sensor_domain, metric_id, measurement_data)
                
                if measurement_domain is not None:
                    self._imported_measurements.append(measurement_domain)
        
        self.info(f'Collected {len(self._imported_sensors)} sensors and {len(self._imported_measurements)} measurements')
        
        sensors_saved = self._sensor_repo.bulk_upsert(
            [sensor_domain for sensor_domain, _ in self._imported_sensors]
        )
        
        self.info(f'Saved {sensors_saved} sensors')
        
        measurements_saved = self._measurement_repo.bulk_upsert(self._imported_measurements)
        
        self.info(f'Saved {measurements_saved} measurements')
    
    def make_sensor(self, sensor_id: str, sensor_data: dict):
        sensor_serializer = SensorSerializer(data=sensor_data)
        
        if not sensor_serializer.is_valid():
            self.error(f'Validation failed for sensor {sensor_id}: {sensor_serializer.errors}')
            return None
        
        validated_sensor = sensor_serializer.validated_data
        sensor_id = int(sensor_id)
        sensor_name = validated_sensor['name']
        type_id = validated_sensor['type']
        variant_id = validated_sensor['variant']
        
        if not sensor_name or sensor_name.strip() == '':
            self.warn(f'Sensor {sensor_id} has empty name. Setting to null')
            sensor_name = None
        
        sensor_type = self._sensor_repo.get_sensor_type(type_id=type_id, variant_id=variant_id)
        
        if sensor_type is None:
            self.warn(f'SensorType not found for type={type_id}, variant={variant_id}. Creating sensor with null type')
        
        sensor_domain = self._sensor_factory.create_sensor(
            id=sensor_id,
            name=sensor_name,
            sensor_type=sensor_type
        )
        
        return (sensor_domain, validated_sensor['metrics'])
    
    def make_measurement(self, sensor_domain, metric_id: str, measurement_data: dict):
        measurement_serializer = MeasurementSerializer(data=measurement_data)
        
        if not measurement_serializer.is_valid():
            self.error(f'Validation failed for measurement in sensor {sensor_domain.id}, metric {metric_id}: {measurement_serializer.errors}')
            return None
        
        validated_measurement = measurement_serializer.validated_data
        timestamp = validated_measurement['t']
        value = validated_measurement['v']
        
        metric = self._measurement_repo.get_metric(int(metric_id))
        
        if metric is None:
            self.warn(f'Metric {metric_id} not found. Skipping measurement for sensor {sensor_domain.id}')
            return None
        
        unit = self._measurement_repo.get_primary_unit_for_metric(metric)
        
        if unit is None:
            self.warn(f'Primary unit not found for metric {metric.name} (ID: {metric_id}). Skipping measurement')
            return None
        
        measured_at = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        measurement_domain = self._measurement_factory.create_measurement(
            sensor=sensor_domain,
            metric=metric,
            unit=unit,
            value=value,
            measured_at=measured_at
        )
        
        return measurement_domain
