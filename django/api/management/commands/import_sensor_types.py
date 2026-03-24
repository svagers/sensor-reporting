import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.repositories import SensorRepository
from api.serializers.sensor_type_import_serializers import SensorTypeJSONSerializer


class Command(BaseCommand):
    help = 'Import sensor types data from JSON file'

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'sensorTypes.json')
        
        if not os.path.exists(json_path):
            raise CommandError(f'File not found: {json_path}')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        serializer = SensorTypeJSONSerializer(data=raw_data)
        
        if not serializer.is_valid():
            self.stdout.write(self.style.ERROR('Validation errors found:'))
            for field, errors in serializer.errors.items():
                self.stdout.write(self.style.ERROR(f'  {field}: {errors}'))
            raise CommandError('JSON validation failed')
        
        validated_data = serializer.validated_data
        repo = SensorRepository()
        
        sensor_types_created = 0
        
        for sensor_type_data in validated_data['sensor_types']:
            type_id = sensor_type_data['type_id']
            variant_id = sensor_type_data['variant_id']
            name = sensor_type_data['name']
            
            repo.create_or_update_sensor_type(
                type_id=type_id,
                variant_id=variant_id,
                name=name
            )
            sensor_types_created += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {sensor_types_created} sensor types!'
        ))
