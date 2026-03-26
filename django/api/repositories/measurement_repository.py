from typing import Optional, List
from django.db import transaction, connection
from pypika import Query, Table, Case
from pypika.functions import Max
from ..models import Measurement, Metric


class MeasurementRepository:
    
    def get_metric(self, metric_id: int) -> Optional[Metric]:
        try:
            return Metric.objects.get(id=metric_id)
        except Metric.DoesNotExist:
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
                }
            )
        return len(measurements)

