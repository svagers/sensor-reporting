from django.core.management.base import CommandError
from api.repositories import MetricRepository
from api.factories import MetricFactory
from api.serializers.metric_import_serializers import MetricSerializer, UnitSerializer
from .base_import_command import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import metrics data from JSON file'

    def __init__(self):
        super().__init__()
        self._metric_repo = MetricRepository()
        self._metric_factory = MetricFactory()
        self._imported_metrics = []
        self._imported_units = []
        self._imported_metric_units = []
    
    def get_json_file_name(self) -> str:
        return 'metrics.json'

    def import_data(self, raw_data: dict) -> None:
        if 'data' not in raw_data or 'items' not in raw_data['data']:
            raise CommandError('Invalid JSON structure: expected "data.items"')

        self.import_metrics(raw_data['data']['items'])
        
        self.info(f'Collected {len(self._imported_metrics)} metrics, {len(self._imported_units)} units, and {len(self._imported_metric_units)} metric-unit links')
        
        metrics_saved = self._metric_repo.bulk_upsert_metrics(self._imported_metrics)
        self.info(f'Saved {metrics_saved} metrics')
        
        units_saved = self._metric_repo.bulk_upsert_units(self._imported_units)
        self.info(f'Saved {units_saved} units')
        
        metric_units_saved = self._metric_repo.bulk_upsert_metric_units(self._imported_metric_units)
        self.info(f'Saved {metric_units_saved} metric-unit links')
    
    def import_metrics(self, raw_data: dict):
        for metric_data in raw_data:
            metric_domain = self.make_metric(metric_data)
            
            if metric_domain is None:
                self.error(f'Failed to create metric')
                continue

            self._imported_metrics.append(metric_domain)
            self.import_units(metric_domain, metric_data.get('units', []))
    
    def import_units(self, metric, raw_data: dict):
        for unit_data in raw_data:
            unit_domain = self.make_unit(unit_data, metric)
            
            if unit_domain is None:
                continue
            
            self._imported_units.append(unit_domain)

            is_primary = unit_data.get('selected', False)
            
            metric_unit = self._metric_factory.create_metric_unit(
                metric_id=metric.id,
                unit_id=unit_domain.id,
                is_primary=is_primary
            )
            
            self._imported_metric_units.append(metric_unit)
    
    def make_metric(self, metric_data: dict):
        metric_serializer = MetricSerializer(data=metric_data)
        
        if not metric_serializer.is_valid():
            self.error(f'Validation failed for metric: {metric_serializer.errors}')
            return None
        
        validated_metric = metric_serializer.validated_data
        
        metric_domain = self._metric_factory.create_metric(
            id=validated_metric['id'],
            name=validated_metric['name']
        )
        
        return metric_domain
    
    def make_unit(self, unit_data: dict, metric):
        unit_serializer = UnitSerializer(data=unit_data)
        
        if not unit_serializer.is_valid():
            self.error(f'Validation failed for unit in metric {metric.name} (#{metric.id}): {unit_serializer.errors}')
            return None
        
        validated_unit = unit_serializer.validated_data
        
        unit_domain = self._metric_factory.create_unit(
            id=validated_unit['id'],
            name=validated_unit['name'],
            precision=validated_unit['precision']
        )
        
        return unit_domain
