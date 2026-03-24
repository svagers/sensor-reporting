from django.db import models


class SensorType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_id = models.IntegerField()
    variant_id = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sensor_types'
        ordering = ['id']
        unique_together = ('type_id', 'variant_id')

    def __str__(self):
        return f"{self.name} (ID: {self.id})"
