from django.db import models


class Sensor(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    sensor_type = models.ForeignKey('SensorType', on_delete=models.CASCADE, related_name='sensors', null=True, blank=True)

    class Meta:
        db_table = 'sensors'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} (ID: {self.id})"
