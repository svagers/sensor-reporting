from rest_framework import serializers


class MeasurementFilterSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    limit = serializers.IntegerField(required=False, default=20, min_value=1, max_value=100)
    sort = serializers.CharField(required=False, allow_blank=True)
    order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    sensor_name = serializers.CharField(required=False, allow_blank=True)
    type_id = serializers.IntegerField(required=False)
    variant_id = serializers.IntegerField(required=False)
    
    def validate(self, data):
        if 'variant_id' in data and 'type_id' not in data:
            raise serializers.ValidationError({
                'variant_id': 'variant_id can only be provided when type_id is present'
            })
        return data
    variant_id = serializers.IntegerField(required=False)
    
    def validate(self, data):
        if 'variant_id' in data and 'type_id' not in data:
            raise serializers.ValidationError({
                'variant_id': 'variant_id can only be provided when type_id is present'
            })
        return data
