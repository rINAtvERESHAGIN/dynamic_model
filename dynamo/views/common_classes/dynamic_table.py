from dynamo.models import *
from dynamo.models.RegisteredModels import RegisteredDynamicModel
from dynamo.models.VariableNamesModel import VariableNameModel
import uuid
from dynamo.models.tree import Instance


# from dynamo.views.task.create_schema import


class DynamicTable:
    table_name = ''
    table_token = ''
    table_uuid = ''
    table_fields = ''

    def __init__(self, json_data, table_name: str) -> None:
        self.json_data = json_data
        self.table_name = table_name

    def register_dynamic_table(self, uuid_model, model, instance) -> None:
        instances = Instance.objects.all()
        print('instance ', instance)
        # проверяем есть ли уже такой instance
        flag = False
        instance_object = ''
        for inst in instances:
            print(inst.instance)
            if inst.instance == instance:
                print("такой истанст есть !")
                # если существует , берем объект
                instance_object = inst
                flag = True
                break
        if not flag:
            # если нет то добавляем новый и берем его id
            print('такой не было')
            instance_object = Instance.objects.create(instance=instance)

        RegisteredDynamicModel.objects.create(dynamic_model=self.table_name,
                                              token=uuid_model,
                                              model=model,
                                              instance=instance_object)

    def table_formation(self) -> 'dynamic table':
        new_schema = MyModel.objects.create(name=self.table_name)

        data = FieldsForModel.objects.create(name='data', data_type='json')
        new_schema.add_field(data, null=True)  # For test TODO сделать что бы json fields могли быть null

        field = FieldsForModel.objects.create(name='field', data_type='character')
        new_schema.add_field(field, null=False, unique=False, max_length=100)

        logged = FieldsForModel.objects.create(name='logged', data_type='date')
        new_schema.add_field(logged)

        type_of = FieldsForModel.objects.create(name='type_of', data_type='character')
        new_schema.add_field(type_of, null=False, unique=False, max_length=50)

        previous = FieldsForModel.objects.create(name='previous', data_type='uuid')
        new_schema.add_field(previous, null=True)

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
