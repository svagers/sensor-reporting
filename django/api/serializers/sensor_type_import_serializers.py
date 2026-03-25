from rest_framework import serializers


class SensorTypeSerializer(serializers.Serializer):
    type_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
