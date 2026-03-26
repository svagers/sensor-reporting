from datetime import datetime
from ..models import Measurement, Sensor, Metric


class MeasurementFactory:
    
    def create_measurement(self, sensor: Sensor, metric: Metric, value: float, measured_at: datetime) -> Measurement:
        measurement = Measurement(
            sensor=sensor,
            metric=metric,
            value=value,
            measured_at=measured_at
        )
        
        return measurement
