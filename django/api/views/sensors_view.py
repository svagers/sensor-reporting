from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.reporters import SensorDataReporter


@extend_schema(
    summary='List sensors with latest measurements',
    description=(
        'Returns one row per sensor. Each row includes `id`, `name`, `type_id` (sensor type '
        'primary key), and dynamic `metric_<id>` columns for metric ids that have measurements '
        '(aggregated with `MAX` for the latest value per sensor and metric).'
    ),
    tags=['Sensors'],
    responses={
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'additionalProperties': True,
                            'description': 'Includes `id`, `name`, `type_id`, metric_* columns',
                        },
                    }
                },
            },
            description='Sensor rows under `data`.',
        )
    },
)
class SensorsView(APIView):
    def get(self, request):
        sensors = SensorDataReporter().report()
        return Response({'data': sensors}, status=status.HTTP_200_OK)
