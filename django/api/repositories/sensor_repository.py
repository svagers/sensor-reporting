from typing import Optional, List
from django.db import transaction
from ..models import Sensor, SensorType


class SensorRepository:
    
    def get_sensor_type(self, type_id: int, variant_id: int) -> Optional[SensorType]:
        try:
            return SensorType.objects.get(type_id=type_id, variant_id=variant_id)
        except SensorType.DoesNotExist:
            return None
    
    def create_or_update_sensor_type(self, type_id: int, variant_id: int, name: str) -> SensorType:
        sensor_type, created = SensorType.objects.update_or_create(
            type_id=type_id,
            variant_id=variant_id,
            defaults={'name': name}
        )
        return sensor_type
    
    def create_or_update_sensor(self, id: int, name: str, sensor_type: SensorType) -> Sensor:
        sensor, created = Sensor.objects.update_or_create(
            id=id,
            defaults={
                'name': name,
                'sensor_type': sensor_type
            }
        )
        return sensor
    
    @transaction.atomic
    def bulk_upsert(self, sensors: List[Sensor]) -> int:
        for sensor in sensors:
            Sensor.objects.update_or_create(
                id=sensor.id,
                defaults={
                    'name': sensor.name,
                    'sensor_type': sensor.sensor_type
                }
            )
        return len(sensors)
