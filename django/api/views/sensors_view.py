from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.reporters import SensorDataReporter


class SensorsView(APIView):
    def get(self, request):
        sensors = SensorDataReporter().report()
        return Response({'data': sensors}, status=status.HTTP_200_OK)
