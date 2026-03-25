from datetime import datetime
from ..models import Measurement, Sensor, Metric, Unit


class MeasurementFactory:
    
    def create_measurement(self, sensor: Sensor, metric: Metric, unit: Unit, value: float, measured_at: datetime) -> Measurement:
        measurement = Measurement(
            sensor=sensor,
            metric=metric,
            unit=unit,
            value=value,
            measured_at=measured_at
        )
        
        return measurement
