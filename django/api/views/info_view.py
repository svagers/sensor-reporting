from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    summary='API info',
    description=(
        'Lightweight JSON status payload. HTML welcome with links is at `/`; OpenAPI '
        'schema at `/api/schema/`; Swagger UI at `/api/docs/`.'
    ),
    tags=['Meta'],
    responses={
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'status': {'type': 'string'},
                    'version': {'type': 'string'},
                },
            },
            description='Service metadata.',
        )
    },
)
class Info(APIView):
    def get(self, request):
        return Response(
            {
                'message': 'Welcome to Saftehnika API',
                'status': 'running',
                'version': '1.0.0',
            }
        )
