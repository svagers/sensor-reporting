from django.db import models


class Unit(models.Model):
    id = models.BigIntegerField(primary_key=True)
    metrics = models.ManyToManyField('Metric', through='MetricUnit', related_name='units')
    name = models.CharField(max_length=100)
    precision = models.IntegerField()

    class Meta:
        db_table = 'units'
        ordering = ['id']

    def __str__(self):
        return self.name
