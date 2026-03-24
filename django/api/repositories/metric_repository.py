from typing import List
from django.db import transaction
from ..models import Metric, Unit, MetricUnit


class MetricRepository:
    
    def create_or_update_metric(self, id: int, name: str) -> Metric:
        metric, created = Metric.objects.update_or_create(
            id=id,
            defaults={'name': name}
        )
        return metric
    
    def create_or_update_unit(self, id: int, name: str, precision: int) -> Unit:
        unit, created = Unit.objects.update_or_create(
            id=id,
            defaults={
                'name': name,
                'precision': precision
            }
        )
        return unit
    
    @transaction.atomic
    def link_unit_metrics(self, unit: Unit, metrics: List[Metric]) -> None:
        metric_ids = [metric.id for metric in metrics]
        
        MetricUnit.objects.filter(unit=unit).exclude(metric_id__in=metric_ids).delete()
        
        for metric in metrics:
            MetricUnit.objects.get_or_create(
                metric=metric,
                unit=unit,
                defaults={'is_primary': False}
            )
    
    @transaction.atomic
    def link_units_to_metric(self, units: List[Unit], metric: Metric) -> None:
        unit_ids = [unit.id for unit in units]
        
        MetricUnit.objects.filter(metric=metric).exclude(unit_id__in=unit_ids).delete()
        
        for unit in units:
            MetricUnit.objects.get_or_create(
                metric=metric,
                unit=unit,
                defaults={'is_primary': False}
            )
    
    @transaction.atomic
    def set_primary_unit(self, metric: Metric, unit: Unit) -> None:
        MetricUnit.objects.filter(metric=metric).update(is_primary=False)
        MetricUnit.objects.update_or_create(
            metric=metric,
            unit=unit,
            defaults={'is_primary': True}
        )
