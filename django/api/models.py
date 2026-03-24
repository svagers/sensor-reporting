from django.db import models


class SensorVariant(models.Model):
    id = models.BigIntegerField(primary_key=True)
    type_id = models.IntegerField()
    variant_id = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sensor_variants'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Metric(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'metrics'
        ordering = ['id']

    def __str__(self):
        return self.name


class Unit(models.Model):
    id = models.BigIntegerField(primary_key=True)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=100)
    precision = models.IntegerField()
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'units'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.metric.name})"


class Sensor(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    sensor_variant = models.ForeignKey(SensorVariant, on_delete=models.CASCADE, related_name='sensors')

    class Meta:
        db_table = 'sensors'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Measurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.FloatField()
    measured_at = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='measurements')

    class Meta:
        db_table = 'measurements'
        ordering = ['measured_at']
        indexes = [
            models.Index(fields=['sensor', 'metric', 'measured_at']),
            models.Index(fields=['measured_at']),
        ]

    def __str__(self):
        return f"{self.sensor.name} - {self.metric.name}: {self.value} at {self.measured_at}"
