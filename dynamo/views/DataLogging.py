from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dynamo.serializers import *
from dynamo.views.task.create_schema import check_model_existence
from dynamo.views.task.log_object import start_log
from django.http.response import JsonResponse


class DataLogging(APIView):

    def post(self, request, instance, app, model):
        serializer = LoggingDataSerializer(data=request.data)
        table_name = instance + app + model
        if check_model_existence(table_name):
            if serializer.is_valid():
                start_log(serializer.data, table_name)
                return JsonResponse(data={'status': 'Got'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
