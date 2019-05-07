from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
from rest_framework.views import APIView
from dynamo.models import *
from rest_framework.response import Response
from rest_framework import status
from dynamo.serializers import *
import datetime
from django.conf import settings
import uuid

"""
Проверка на token и поля
"""


class ApiEntryPoint(View):
    _token = None
    required = []

    def check_post_data(self, request: HttpRequest):
        for field in self.required:
            if field not in request.POST:
                return False
        return True

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if 'token' in request.POST:
            token = request.POST.get('token', None)
            if token == settings.API_TOKEN:
                self._token = token
                if self.check_post_data(request):
                    return super().dispatch(request, *args, **kwargs)
        return HttpResponseBadRequest()


# Create your views here.
# class CreatingSchemaSignal(APIView):
#     # http://127.0.0.1:8000/logging/create_schema/
#     table_name = ''
#
#     def post(self, request, instance, app, model):
#         print('In method post')
#         serializer = CreateNewSchemaSerializer(data=request.data)
#         if serializer.is_valid():
#             print(serializer.data)
#             self.table_name = instance + app + model
#             if self.check_model_existence():
#                 print('Модель уже существует')
#                 return HttpResponseBadRequest()
#             else:
#                 # таблица
#                 new_schema = MyModel.objects.create(name=self.table_name)
#                 # поле - хранит данные
#                 data = FieldsForModel.objects.create(name='data', data_type='json')
#                 new_schema.add_field(data)
#                 # поле - хранит время создания лога объекта
#                 logged = FieldsForModel.objects.create(name='logged', data_type='date')
#                 new_schema.add_field(logged)
#                 # поле - хранит тип действия над объектом
#                 type_of = FieldsForModel.objects.create(name='type_of', data_type='character')
#                 new_schema.add_field(type_of, null=False, unique=False, max_length=50)
#                 # previous данные которые были до изменения
#                 previous = FieldsForModel.objects.create(name='previous', data_type='json')
#                 new_schema.add_field(previous)
#                 # changed - дата когда объект был изменен
#                 changed = FieldsForModel.objects.create(name='changed', data_type='date')
#                 new_schema.add_field(changed)
#                 # uuid = object - UUID объекта который приходит для логирования -
#                 # ( в будещем используеются для восстановления )
#                 object_uuid = FieldsForModel.objects.create(name='object_uuid', data_type='uuid')
#                 new_schema.add_field(object_uuid)
#                 # uuid самой записи
#                 record_uuid = FieldsForModel.objects.create(name='record_uuid', data_type='uuid')
#                 new_schema.add_field(record_uuid)
#
#                 Table = new_schema.as_model()
#
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def check_model_existence(self):
#         is_exist = False
#         try:
#             print('Search for ' + self.table_name)
#             is_model_existence = MyModel.objects.get(name=self.table_name)
#             is_exist = True
#         except Exception:
#             is_exist = False
#             print('Model do not exist!')
#
#         return is_exist


# class DataLoggingSignal(APIView):
#     # http://127.0.0.1:8000/logging/data_log/
#
#     # required = [
#     #     'sender',
#     #     'data',
#     #     'type',
#     # ]
#
#     table_name = ''
#     object_uuid = uuid.uuid4()
#
#     def post(self, request, instance, app, model):
#         serializer = LoggingDataSerializer(data=request.data)
#         if serializer.is_valid():
#             self.table_name = instance + app + model
#             model_schema = MyModel.objects.get(name=self.table_name)
#             table_schema = model_schema.as_model()
#             # from json
#             data = serializer.data.pop('data')
#             type_of = serializer.data.pop('type_of')
#             self.object_uuid = serializer.data.pop('object_uuid')
#             changed = serializer.data.pop('changed')
#             previous = self.find_previous()
#             # generate
#             record_uuid = uuid.uuid4()
#             table_schema.objects.create(data=data,  # json # data for log
#                                         logged=datetime.datetime.now(),  # time when log is writen
#                                         type_of=type_of,  # json  # type of signal
#                                         object_uuid=self.object_uuid,  # json  # object uuid that come from instance
#                                         changed=changed,  # json  # time when object changed in front
#                                         record_uuid=record_uuid,  # my own uuid
#                                         # for test
#                                         previous=previous,
#                                         )
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def find_previous(self):
#         # получаем предыдущие актуальные данные
#         # которые будут предыдущими для нового объекта.
#         schema_ = MyModel.objects.get(name=self.table_name)
#         model_for = schema_.as_model()
#         try:
#             all_data_on_uuid = model_for.objects.filter(object_uuid__lte=self.object_uuid).order_by('-id')[0]
#             previous = all_data_on_uuid.data
#         except Exception:
#             print("What!")
#         return previous
#
#
