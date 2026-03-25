from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import MeasurementFilterSerializer
from api.reporters import SensorDataReporter


class MeasurementsView(APIView):
    def post(self, request):
        serializer = MeasurementFilterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sensor_data_reporter = SensorDataReporter()
        validated_filter = serializer.validated_data
        measurements = sensor_data_reporter.report(validated_filter)
        
        data = {
            'data': measurements,
            'filters': validated_filter,
        }
        return Response(data, status=status.HTTP_200_OK)
