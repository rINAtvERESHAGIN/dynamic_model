from rest_framework.views import APIView
from dynamo.models import *
from rest_framework.response import Response
from rest_framework import status
from dynamo.serializers import *
import datetime
import uuid
from django.contrib.postgres import fields


class DataLogging(APIView):
    # http://127.0.0.1:8000/logging/data_log/

    # required = [
    #     'sender',
    #     'data',
    #     'type',
    # ]

    table_name = ''
    object_uuid = uuid.uuid4()
    changed = datetime.datetime.now()
    data = ''
    previous = ''
    data_dict = ''
    field = ''

    def post(self, request, instance, app, model):
        serializer = LoggingDataSerializer(data=request.data)
        self.data_dict = request.data
        if serializer.is_valid():
            self.table_name = instance + app + model
            model_schema = MyModel.objects.get(name=self.table_name)
            table_schema = model_schema.as_model()
            # from json
            self.data = serializer.data.pop('data')
            type_of = serializer.data.pop('type_of')
            self.object_uuid = serializer.data.pop('object_uuid')
            self.changed = serializer.data.pop('changed')

            self.set_and_parse_json_key()

            if self.check_by_changed():
                print('Хронология восстановлена')
            else:
                print('Хронология не нарушина')
                self.previous = self.find_previous()
            # generate
            record_uuid = uuid.uuid4()

            table_schema.objects.create(data=self.data,  # json # data for log
                                        field=self.field,
                                        logged=datetime.datetime.now(),  # time when log is writen
                                        type_of=type_of,  # json  # type of signal
                                        object_uuid=self.object_uuid,  # json  # object uuid that come from instance
                                        changed=self.changed,  # json  # time when object changed in front
                                        record_uuid=record_uuid,  # my own uuid
                                        previous=self.previous,
                                        )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO сделать нахождение предыдущего по uuid и по полю fields ГОТОВО
    # TODO сделать проверку на то что такого ключа нет и если такого ключа нет previous будет null ГОТОВО

    def find_previous(self):
        # получаем актуальные данные которые будут предыдущими для нового объекта.
        schema_ = MyModel.objects.get(name=self.table_name)
        model_for = schema_.as_model()
        number_of_field = model_for.objects.filter(field__exact=self.field)
        if number_of_field.__len__() > 0:
            try:
                object_on_uuid = model_for.objects.filter(object_uuid__lte=self.object_uuid
                                                            ).filter(field__exact=self.field
                                                                     ).order_by('-changed')[0]
                previous = object_on_uuid.record_uuid
            except Exception:
                print("What!")
            return previous
        else:
            return None

    # TODO поправить восстановление хронологии включая поле field ГОТОВО
    def check_by_changed(self):

        schema_ = MyModel.objects.get(name=self.table_name)
        model_ = schema_.as_model()

        all_found = model_.objects.filter(object_uuid__lte=self.object_uuid
                                          ).filter(field__exact=self.field
                                                   ).order_by('id')
        # TODO доработка принятия времени
        changed_time = datetime.datetime.strptime(self.changed, '%Y-%m-%d')
        flag = False
        for record in all_found:
            if record.changed > changed_time:
                hurried_object = record
                tmp_previous = hurried_object.previous
                # сохранненому объекту ( который старше по времени ) меняет previous на данные входящего
                model_.objects.filter(pk=hurried_object.id).update(previous=self.data)
                # входящему объекту ставим previous который был автоматически поставлен сохраненному объекту
                self.previous = tmp_previous
                flag = True
                break
        if flag:
            return True
        else:
            return False

    def set_and_parse_json_key(self):
        for key in self.data.keys():
            key_name = key
            self.field = key_name
        return key_name
