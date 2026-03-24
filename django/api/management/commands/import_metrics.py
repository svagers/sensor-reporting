import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.repositories import MetricRepository
from api.serializers import MetricsJSONSerializer


class Command(BaseCommand):
    help = 'Import metrics data from JSON file'

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'metrics.json')
        
        if not os.path.exists(json_path):
            raise CommandError(f'File not found: {json_path}')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        serializer = MetricsJSONSerializer(data=raw_data)
        
        if not serializer.is_valid():
            self.stdout.write(self.style.ERROR('Validation errors found:'))
            for field, errors in serializer.errors.items():
                self.stdout.write(self.style.ERROR(f'  {field}: {errors}'))
            raise CommandError('JSON validation failed')
        
        validated_data = serializer.validated_data
        repo = MetricRepository()
        
        metrics_created = 0
        units_created = 0
        
        for metric_data in validated_data['data']['items']:
            metric_id = metric_data['id']
            metric_name = metric_data['name']
            
            metric = repo.create_or_update_metric(id=metric_id, name=metric_name)
            metrics_created += 1
            
            units = []
            primary_unit = None
            
            for unit_data in metric_data['units']:
                unit_id = unit_data['id']
                unit_name = unit_data['name']
                precision = unit_data['precision']
                is_primary = unit_data.get('selected', False)
                
                unit = repo.create_or_update_unit(
                    id=unit_id,
                    name=unit_name,
                    precision=precision
                )
                units.append(unit)
                units_created += 1
                
                if is_primary and primary_unit is not None:
                    self.stdout.write(self.style.WARNING(
                        f'Multiple primary units found for metric "{metric_name}" (ID: {metric_id}). '
                        f'Using last one: {unit_name} (ID: {unit_id})'
                    ))
                
                if is_primary:
                    primary_unit = unit
            
            repo.link_units_to_metric(units=units, metric=metric)
            
            if primary_unit:
                repo.set_primary_unit(metric=metric, unit=primary_unit)
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {metrics_created} metrics and {units_created} units!'
        ))
