from pypika import Query, Table, Case
from pypika.functions import Max
from typing import List
from django.db import connection
from ..models import Measurement


class SensorDataReporter:
    def __init__(self):
        self._sensors = Table('sensors')
        self._sensor_types = Table('sensor_types')
        self._measurements = Table('measurements')
    
    def report(self):
        self._build_base_query()
        return self._execute()
    
    def _build_base_query(self):
        self._base_query = Query.from_(self._sensors).left_join(self._sensor_types).on(
            self._sensors.sensor_type_id == self._sensor_types.id
        ).left_join(self._measurements).on(
            self._sensors.id == self._measurements.sensor_id
        ).select(self._sensors.id, self._sensors.name, self._sensor_types.id.as_('type_id'))

        metric_ids = self._get_used_metric_ids()

        for metric_id in metric_ids:
            metric_column = Max(
                Case()
                .when(self._measurements.metric_id == metric_id, self._measurements.value)
            ).as_(f'metric_{metric_id}')
            self._base_query = self._base_query.select(metric_column)
        
        self._base_query = self._base_query.groupby(
            self._sensors.id,
            self._sensors.name,
            self._sensor_types.id
        )

    def _execute(self):
        sql = str(self._base_query)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    
    def _get_used_metric_ids(self) -> List[int]:
        return list(set(Measurement.objects.values_list('metric_id', flat=True)))
        
    