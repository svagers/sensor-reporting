from django.contrib import admin
from .models import SensorType, Metric, Unit, MetricUnit, Sensor, Measurement


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type_id', 'variant_id']
    list_filter = ['type_id', 'variant_id']
    search_fields = ['name', 'id']


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name', 'id']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'precision']
    search_fields = ['name', 'id']


@admin.register(MetricUnit)
class MetricUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'metric', 'unit', 'is_primary']
    list_filter = ['is_primary', 'metric']
    search_fields = ['metric__name', 'unit__name']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sensor_type']
    list_filter = ['sensor_type']
    search_fields = ['name', 'id']


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'sensor', 'metric', 'value', 'measured_at']
    list_filter = ['sensor', 'metric', 'measured_at']
    search_fields = ['id']
    date_hierarchy = 'measured_at'
