from typing import List
from django.db import transaction
from ..models import Metric, Unit, MetricUnit


class MetricRepository:
    
    def get_used_metrics(self) -> List[dict]:
        metrics = Metric.objects.filter(
            measurements__isnull=False
        ).distinct().prefetch_related('metricunit_set__unit')
        
        return [
            {
                'id': metric.id,
                'name': metric.name,
                'primary_unit': {
                    'id': primary.unit.id,
                    'name': primary.unit.name,
                    'precision': primary.unit.precision
                } if (primary := next((metric_unit for metric_unit in metric.metricunit_set.all() if metric_unit.is_primary), None)) else None
            }
            for metric in metrics
        ]
    
    @transaction.atomic
    def bulk_upsert_metrics(self, metrics: List[Metric]) -> int:
        for metric in metrics:
            Metric.objects.update_or_create(
                id=metric.id,
                defaults={'name': metric.name}
            )
        return len(metrics)
    
    @transaction.atomic
    def bulk_upsert_units(self, units: List[Unit]) -> int:
        for unit in units:
            Unit.objects.update_or_create(
                id=unit.id,
                defaults={
                    'name': unit.name,
                    'precision': unit.precision
                }
            )
        return len(units)
    
    @transaction.atomic
    def bulk_upsert_metric_units(self, metric_units: List[MetricUnit]) -> int:
        for metric_unit in metric_units:
            MetricUnit.objects.update_or_create(
                metric_id=metric_unit.metric_id,
                unit_id=metric_unit.unit_id,
                defaults={'is_primary': metric_unit.is_primary}
            )
        return len(metric_units)
