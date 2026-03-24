from django.db import models


class Metric(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'metrics'
        ordering = ['id']

    def __str__(self):
        return self.name
