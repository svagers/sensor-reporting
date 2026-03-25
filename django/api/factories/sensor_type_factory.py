from ..models import SensorType


class SensorTypeFactory:
    
    def create_sensor_type(self, type_id: int, variant_id: int, name: str) -> SensorType:
        sensor_type = SensorType(
            type_id=type_id,
            variant_id=variant_id,
            name=name
        )
        
        return sensor_type
