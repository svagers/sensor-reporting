from rest_framework import serializers


class SensorTypeVariantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class SensorTypeJSONSerializer(serializers.Serializer):
    
    def to_internal_value(self, data):
        sensor_types = []
        
        for type_id, variants in data.items():
            for variant_id, variant_data in variants.items():
                sensor_type = {
                    'type_id': int(type_id),
                    'variant_id': int(variant_id),
                    'name': variant_data.get('name', '')
                }
                sensor_types.append(sensor_type)
        
        return {'sensor_types': sensor_types}
