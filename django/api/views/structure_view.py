from rest_framework.views import APIView
from rest_framework.response import Response
from api.repositories.sensor_repository import SensorRepository
from api.repositories.metric_repository import MetricRepository


class StructureView(APIView):
    def get(self, request):
        sensor_repository = SensorRepository()
        metric_repository = MetricRepository()
        
        sensor_types = sensor_repository.get_used_sensor_types()
        metrics = metric_repository.get_used_metrics()
        
        return Response({
            'sensor_types': sensor_types,
            'metrics': metrics
        })
