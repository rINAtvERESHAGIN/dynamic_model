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
from dynamo.models.VariableNamesModel import VariableNameModel
from dynamo.models.RegisteredModels import RegisteredDynamicModel
from dynamo.serializers import RestoringObjectSerializer

"""

"""


# TODO в request будет идти uuid объекта который нужно восстановить, поэтому поис его данныех будет по его полю ГОТОВО
class RestoringObject(APIView):
    table_name = ''
    object_uuid = ''

    def post(self, request, instance, app, model):
        serializer = RestoringObjectSerializer(data=request.data)
        if serializer.is_valid():
            self.table_name = instance + app + model
            self.object_uuid = serializer.data.pop('object_uuid')

            recovered_object_data = self.find_actual_data()
            return JsonResponse(data={
                "object": self.object_uuid,
                "model": model,
                "instance": instance,
                "data": recovered_object_data
            })

    """
    1.По имени таблицы находим запись о таблице в модели разегестрированных динамический моделей
    2.Получаем их токен 
    3.По токену в таблице которая хранит поля этих таблиц находим все поля 
    4.Находим динамическую таблицу 
    5.По uuid объекта который нужно восстановить , находим все записи
        a. Фильтруем по имени полю
        b. Берем последнюю запись
    6.Собираем объект 
    """
    # TODO т.к. при создание динамической таблицы будут приходить и все ее поля , но если это поле никак не было
    # TODO изменено ( или мне будут загружать все актуальные данные ) , если так то все будет работать.
    
    def find_actual_data(self):
        incoming_table_name = self.table_name  # - получил имя таблицы с запроса
        try:
            table_entry = RegisteredDynamicModel.objects.get(model_name__exact=incoming_table_name)
        except Exception:
            print('Could not find record about this schema!')

        token_for_incoming_table = table_entry.token
        all_entries_for_this_model = VariableNameModel.objects.filter(uuid_model__lte=token_for_incoming_table)
        var_name_list = []

        for record in all_entries_for_this_model:
            var_name_list.append(record.name)

        schema_test = MyModel.objects.get(name=self.table_name)
        model_test = schema_test.as_model()
        object_to_send = {}

        for var in var_name_list:
            value = model_test.objects.filter(object_uuid__lte=self.object_uuid
                                              ).filter(field__exact=var
                                                       ).order_by('-changed')[0]
            current_value = value.data.pop(var)
            object_to_send[var] = current_value
        return object_to_send
