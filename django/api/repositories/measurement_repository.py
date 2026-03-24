from typing import List, Optional
from django.db import transaction
from ..models import Measurement


class MeasurementRepository:
    
    def create(self, **kwargs) -> Measurement:
        return Measurement.objects.create(**kwargs)
    
    def get_by_id(self, id: int) -> Optional[Measurement]:
        try:
            return Measurement.objects.get(id=id)
        except Measurement.DoesNotExist:
            return None
    
    def get_all(self) -> List[Measurement]:
        return list(Measurement.objects.all())
    
    def get_by_sensor(self, sensor_id: int) -> List[Measurement]:
        return list(Measurement.objects.filter(sensor_id=sensor_id))
    
    def get_by_metric(self, metric_id: int) -> List[Measurement]:
        return list(Measurement.objects.filter(metric_id=metric_id))
    
    @transaction.atomic
    def bulk_create(self, items: List[dict]) -> List[Measurement]:
        objects = [Measurement(**item) for item in items]
        return Measurement.objects.bulk_create(objects, ignore_conflicts=True)
