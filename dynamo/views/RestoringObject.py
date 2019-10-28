from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from dynamo.serializers import RestoringObjectSerializer
from dynamo.views.task.actual_data import find_actual_data
from dynamo.views.task.create_schema import check_model_existence

"""

"""


class RestoringObject(APIView):

    def post(self, request, instance, app, model):
        print(request.data)
        serializer = RestoringObjectSerializer(data=request.data)
        table_name = instance + app + model
        if check_model_existence(table_name):
            if serializer.is_valid():
                object_uuid = serializer.data.pop('object_uuid')
                find_actual_data(table_name, object_uuid, model, instance)
                return JsonResponse(data={'status': 'init'})
        else:
            return JsonResponse(data={'status': 'model do not exist'})
