from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dynamo.serializers import *
from dynamo.views.task.create_schema import create_table
from django.http.response import JsonResponse


class Register(APIView):
    def post(self, request, instance, app, model):
        serializer = CreateNewSchemaSerializer(data=request.data)
        if serializer.is_valid():
            # имена таблицы
            table_name = instance + app + model
            create_table(serializer.data, table_name, model, instance)
            return JsonResponse(data={'status': 'Got'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
