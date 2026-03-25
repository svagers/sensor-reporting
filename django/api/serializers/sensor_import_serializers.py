from rest_framework import serializers


class MeasurementSerializer(serializers.Serializer):
    t = serializers.IntegerField()
    v = serializers.FloatField()


class SensorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=True)
    type = serializers.IntegerField()
    variant = serializers.IntegerField()
    metrics = serializers.DictField(child=MeasurementSerializer())
