from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.reporters import SensorDataReporter


class MeasurementsView(APIView):
    def get(self, request):
        xxx
        measurements = SensorDataReporter().report()
        return Response({'data': measurements}, status=status.HTTP_200_OK)
