from ..models import Metric, Unit, MetricUnit


class MetricFactory:
    
    def create_metric(self, id: int, name: str) -> Metric:
        metric = Metric(
            id=id,
            name=name
        )
        
        return metric
    
    def create_unit(self, id: int, name: str, precision: int) -> Unit:
        unit = Unit(
            id=id,
            name=name,
            precision=precision
        )
        
        return unit
    
    def create_metric_unit(self, metric_id: int, unit_id: int, is_primary: bool) -> MetricUnit:
        metric_unit = MetricUnit(
            metric_id=metric_id,
            unit_id=unit_id,
            is_primary=is_primary
        )
        
        return metric_unit
