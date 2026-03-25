from api.repositories import SensorRepository
from api.factories import SensorTypeFactory
from api.serializers.sensor_type_import_serializers import SensorTypeSerializer
from .base_import_command import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import sensor types data from JSON file'

    def __init__(self):
        super().__init__()
        self._sensor_repo = SensorRepository()
        self._sensor_type_factory = SensorTypeFactory()
        self._imported_sensor_types = []
    
    def get_json_file_name(self) -> str:
        return 'sensorTypes.json'

    def import_data(self, raw_data: dict) -> None:
        for type_id, variants in raw_data.items():
            for variant_id, variant_data in variants.items():
                sensor_type_domain = self.make_sensor_type({
                    'type_id': int(type_id),
                    'variant_id': int(variant_id),
                    'name': variant_data.get('name', '')
                })
                
                if sensor_type_domain is None:
                    self.error(f'Failed to create sensor type for type={type_id}, variant={variant_id}')
                    continue
                
                self._imported_sensor_types.append(sensor_type_domain)
        
        self.info(f'Collected {len(self._imported_sensor_types)} sensor types')
        
        sensor_types_saved = self._sensor_repo.bulk_upsert_sensor_types(self._imported_sensor_types)
        
        self.info(f'Saved {sensor_types_saved} sensor types')
    
    def make_sensor_type(self, sensor_type_data: dict):
        sensor_type_serializer = SensorTypeSerializer(data=sensor_type_data)
        
        if not sensor_type_serializer.is_valid():
            self.error(f'Validation failed for sensor type: {sensor_type_serializer.errors}')
            return None
        
        validated_sensor_type = sensor_type_serializer.validated_data
        
        sensor_type_domain = self._sensor_type_factory.create_sensor_type(
            type_id=validated_sensor_type['type_id'],
            variant_id=validated_sensor_type['variant_id'],
            name=validated_sensor_type['name']
        )
        
        return sensor_type_domain
