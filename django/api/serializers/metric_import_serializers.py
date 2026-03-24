from rest_framework import serializers


class UnitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100, allow_blank=True)
    precision = serializers.IntegerField()
    selected = serializers.BooleanField(default=False, required=False)


class MetricSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    units = UnitSerializer(many=True)


class MetricsDataSerializer(serializers.Serializer):
    lang = serializers.CharField(required=False)
    currentItemCount = serializers.IntegerField(required=False)
    items = MetricSerializer(many=True)


class MetricsJSONSerializer(serializers.Serializer):
    data = MetricsDataSerializer()
