from typing import Optional, List
from django.db import transaction, connection
from pypika import Query, Table, Case
from pypika.functions import Max
from ..models import Measurement, Metric, Unit, MetricUnit


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
    
    @transaction.atomic
    def bulk_upsert(self, measurements: List[Measurement]) -> int:
        for measurement in measurements:
            Measurement.objects.update_or_create(
                sensor=measurement.sensor,
                metric=measurement.metric,
                defaults={
                    'value': measurement.value,
                    'measured_at': measurement.measured_at,
                    'unit': measurement.unit
                }
            )
        return len(measurements)

