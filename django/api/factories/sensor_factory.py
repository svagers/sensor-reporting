from typing import Optional
from ..models import Sensor, SensorType


class SensorFactory:
    
    def create_sensor(self, id: int, name: Optional[str], sensor_type: Optional[SensorType]) -> Sensor:
        sensor = Sensor(
            id=id,
            name=name,
            sensor_type=sensor_type
        )
        
        return sensor
