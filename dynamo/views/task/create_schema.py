from background_task import background
from dynamo.models.models import MyModel
import uuid
from dynamo.views.common_classes.dynamic_table import DynamicTable


@background(schedule=10)
def create_table(json_data, table_name, model, instance):
    dynamic_table = DynamicTable(json_data, table_name)
    # проверка на существования такой таблицы
    if check_model_existence(table_name):
        print('is_exist(): return True')
        # return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        # получаем поля которые есть у таблицы
        dynamic_table.table_fields = json_data.pop('table_fields')
        # создаем uuid динамической таблицы
        uuid_model = generate_token()
        # регестрируем динамическую таблицу
        dynamic_table.register_dynamic_table(uuid_model=uuid_model, model=model, instance=instance)
        # вытаскиваем все поля в таблице
        dynamic_table.get_table_fields(uuid_model)
        # формируем таблицу и создаем
        dynamic_table.table_formation().as_model()
        print('Table create')


def check_model_existence(table_name):
    try:
        MyModel.objects.get(name=table_name)
        is_exist = True
    except Exception:
        is_exist = False
    return is_exist


def generate_token():
    return uuid.uuid4()
