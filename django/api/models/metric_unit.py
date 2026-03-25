from django.db import models


class MetricUnit(models.Model):
    metric = models.ForeignKey('Metric', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'metric_units'
        unique_together = ('metric', 'unit')
        constraints = [
            models.UniqueConstraint(
                fields=['metric'],
                condition=models.Q(is_primary=True),
                name='unique_primary_unit_per_metric'
            )
        ]

    def __str__(self):
        return f"{self.unit.name} for {self.metric.name} (primary: {self.is_primary})"
