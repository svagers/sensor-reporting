from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from api.repositories.metric_repository import MetricRepository
from api.repositories.sensor_repository import SensorRepository


@extend_schema(
    summary='Sensor types and metrics in use',
    description=(
        'Returns sensor types that have at least one sensor, and metrics that have at least '
        'one measurement. Used to drive the UI (filters, columns, units).'
    ),
    tags=['Structure'],
    responses={
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'sensor_types': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'type_id': {'type': 'integer'},
                                'variant_id': {'type': 'integer'},
                                'name': {'type': 'string'},
                            },
                        },
                    },
                    'metrics': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'primary_unit': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'precision': {'type': 'integer'},
                                    },
                                },
                            },
                        },
                    },
                },
            },
            description='Sensor types and metrics with primary units.',
        )
    },
)
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
