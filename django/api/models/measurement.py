from django.db import models


class Measurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.FloatField()
    measured_at = models.DateTimeField()
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='measurements')
    metric = models.ForeignKey('Metric', on_delete=models.CASCADE, related_name='measurements')
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='measurements')

    class Meta:
        db_table = 'measurements'
        ordering = ['measured_at']
        unique_together = ('measured_at', 'metric', 'unit')
        indexes = [
            models.Index(fields=['sensor', 'metric', 'measured_at']),
            models.Index(fields=['measured_at']),
        ]

    def __str__(self):
        return f"{self.sensor.name} - {self.metric.name}: {self.value} at {self.measured_at}"
