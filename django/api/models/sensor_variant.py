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
