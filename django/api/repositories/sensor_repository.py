from typing import Optional, List
from django.db import transaction
from ..models import Sensor, SensorType


class SensorRepository:
    
    def get_sensor_type(self, type_id: int, variant_id: int) -> Optional[SensorType]:
        try:
            return SensorType.objects.get(type_id=type_id, variant_id=variant_id)
        except SensorType.DoesNotExist:
            return None
    
    def get_used_sensor_types(self) -> List[dict]:
        sensor_types = SensorType.objects.filter(
            sensors__isnull=False
        ).distinct().values('id', 'type_id', 'variant_id', 'name')
        
        return list(sensor_types)
    
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
    
    @transaction.atomic
    def bulk_upsert_sensor_types(self, sensor_types: List[SensorType]) -> int:
        for sensor_type in sensor_types:
            SensorType.objects.update_or_create(
                type_id=sensor_type.type_id,
                variant_id=sensor_type.variant_id,
                defaults={'name': sensor_type.name}
            )
        return len(sensor_types)
