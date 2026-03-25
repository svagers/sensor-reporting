from datetime import datetime
from typing import Optional, List
from django.db import transaction
from ..models import Measurement, Sensor, Metric, Unit, MetricUnit


class MeasurementRepository:
    
    def get_metric(self, metric_id: int) -> Optional[Metric]:
        try:
            return Metric.objects.get(id=metric_id)
        except Metric.DoesNotExist:
            return None
    
    def get_primary_unit_for_metric(self, metric: Metric) -> Optional[Unit]:
        try:
            metric_unit = MetricUnit.objects.get(metric=metric, is_primary=True)
            return metric_unit.unit
        except MetricUnit.DoesNotExist:
            return None
    
    def create_or_update_measurement(self, sensor: Sensor, metric: Metric, unit: Unit, value: float, measured_at: datetime) -> Measurement:
        measurement, created = Measurement.objects.update_or_create(
            measured_at=measured_at,
            metric=metric,
            unit=unit,
            defaults={
                'sensor': sensor,
                'value': value
            }
        )
        return measurement
    
    @transaction.atomic
    def bulk_upsert(self, measurements: List[Measurement]) -> int:
        for measurement in measurements:
            Measurement.objects.update_or_create(
                measured_at=measurement.measured_at,
                metric=measurement.metric,
                unit=measurement.unit,
                defaults={
                    'sensor': measurement.sensor,
                    'value': measurement.value
                }
            )
        return len(measurements)
