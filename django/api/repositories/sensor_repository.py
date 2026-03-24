from ..models import SensorType


class SensorRepository:
    
    def create_or_update_sensor_type(self, type_id: int, variant_id: int, name: str) -> SensorType:
        sensor_type, created = SensorType.objects.update_or_create(
            type_id=type_id,
            variant_id=variant_id,
            defaults={'name': name}
        )
        return sensor_type
