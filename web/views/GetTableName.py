from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView
from dynamo.models.models import MyModel
from web.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from dynamo.models.tree import Instance
from dynamo.models.RegisteredModels import RegisteredDynamicModel


class TreeViews:
    def __init__(self, instance, model):
        self.instance = instance
        self.model = model


class GetTableName(ListAPIView):
    serializer_class = InstanceSerializer
    queryset = Instance.objects


class SendDynamicData(APIView):
    table_name = ''

    # принимаем имя таблицы объектом MyModel()
    def post(self, request):
        print(request.data)
        serializer = RegisteredModelSerializer(data=request.data)
        if serializer.is_valid():
            self.table_name = serializer.data.pop('dynamic_model')
            record_about_dynamic_model = MyModel.objects.get(name=self.table_name)

            dynamic_model = record_about_dynamic_model.as_model()
            all_data = dynamic_model.objects.all().order_by('id')

            to_send = {}
            list_test = []
            for record in all_data:
                id = record.id
                field = record.field
                data = record.data.pop(field)
                # previous_data = dynamic_model.objects.filter(record_uuid__exact=record.previous)
                if record.previous is None:
                    previous = 'None'
                    pass
                else:
                    previous_data = dynamic_model.objects.get(record_uuid=record.previous)
                    previous = previous_data.data.pop('name')
                changed = record.changed
                logged = record.logged
                object_uuid = record.object_uuid

                t = TableListModal(id, field, data, previous, changed, logged, object_uuid)
                list_test.append(t)
            table_list_serializer = DynamicModelSerializer(list_test, many='True')
            print(table_list_serializer.data)
            return Response(table_list_serializer.data)
        else:
            print('Something wrong')


class TableListModal:

    def __init__(self, r_id, field, data, previous, changed, logged, object_uuid):
        self.id = r_id
        self.field = field
        self.data = data
        self.previous = previous
        self.changed = changed
        self.logged = logged
        self.object_uuid = object_uuid
