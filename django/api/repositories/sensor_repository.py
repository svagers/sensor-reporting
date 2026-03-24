from typing import List, Optional
from django.db import transaction
from ..models import Sensor


class SensorRepository:
    
    def create(self, **kwargs) -> Sensor:
        return Sensor.objects.create(**kwargs)
    
    def get_by_id(self, id: int) -> Optional[Sensor]:
        try:
            return Sensor.objects.get(id=id)
        except Sensor.DoesNotExist:
            return None
    
    def get_all(self) -> List[Sensor]:
        return list(Sensor.objects.all())
    
    @transaction.atomic
    def bulk_create(self, items: List[dict]) -> List[Sensor]:
        objects = [Sensor(**item) for item in items]
        return Sensor.objects.bulk_create(objects, ignore_conflicts=True)
