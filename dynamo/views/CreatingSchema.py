from django.http.response import HttpResponseBadRequest
from rest_framework.views import APIView
from dynamo.models import *
from rest_framework.response import Response
from rest_framework import status
from dynamo.serializers import *
from dynamo.models.RegisteredModels import RegisteredDynamicModel
from dynamo.models.VariableNamesModel import VariableNameModel
import uuid


class CreatingSchema(APIView):
    # http://127.0.0.1:8000/logging/create_schema/
    table_name = ''
    table_token = ''
    table_uuid = ''
    table_fields = ''

    def post(self, request, instance, app, model):
        serializer = CreateNewSchemaSerializer(data=request.data)
        if serializer.is_valid():
            self.table_name = instance + app + model
            if self.check_model_existence():
                print('Модель уже существует')
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                self.table_fields = serializer.data.pop('table_fields')
                uuid_model = self.generate_token()
                print(uuid_model)
                self.register_dynamic_table(uuid_model)

                self.get_table_fields(uuid_model)

                self.table_formation().as_model()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_model_existence(self):
        is_exist = False
        try:
            print('Search for ' + self.table_name)
            MyModel.objects.get(name=self.table_name)
            is_exist = True
        except Exception:
            is_exist = False
            print('Model do not exist!')

        return is_exist

    def register_dynamic_table(self, uuid_model):
        RegisteredDynamicModel.objects.create(model_name=self.table_name, token=uuid_model)

    def generate_token(self):
        return uuid.uuid4()

    def table_formation(self):
        new_schema = MyModel.objects.create(name=self.table_name)

        data = FieldsForModel.objects.create(name='data', data_type='json')
        new_schema.add_field(data, null=True)  # For test TODO сделать что бы json fields могли быть null

        field = FieldsForModel.objects.create(name='field', data_type='character')
        new_schema.add_field(field, null=False, unique=False, max_length=100)

        logged = FieldsForModel.objects.create(name='logged', data_type='date')
        new_schema.add_field(logged)

        type_of = FieldsForModel.objects.create(name='type_of', data_type='character')
        new_schema.add_field(type_of, null=False, unique=False, max_length=50)

        previous = FieldsForModel.objects.create(name='previous', data_type='json')
        new_schema.add_field(previous)

        changed = FieldsForModel.objects.create(name='changed', data_type='date')
        new_schema.add_field(changed)

        object_uuid = FieldsForModel.objects.create(name='object_uuid', data_type='uuid')
        new_schema.add_field(object_uuid)

        record_uuid = FieldsForModel.objects.create(name='record_uuid', data_type='uuid')
        new_schema.add_field(record_uuid)

        return new_schema

    def get_table_fields(self, uuid_model):
        for field in self.table_fields.values():
            VariableNameModel.objects.create(name=field, uuid_model=uuid_model)
