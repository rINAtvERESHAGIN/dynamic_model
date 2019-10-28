from dynamo.models import *
from dynamo.models.VariableNamesModel import VariableNameModel
from dynamo.models.RegisteredModels import RegisteredDynamicModel
from background_task import background
import requests
"""
# - получил имя таблицы с запроса
# пробуем найти таблицу
# находим все поля для этой таблицы
# получаем token таблицы который генерируется при ее создание
# лист в котором будут храниться все имена полей
# проходимся по всем найденым полям и записываем их в лист который хранит имена полей таблицы
# находим таблицу по имени
# делаем ее моделью django
    # будущий словарь
# собриаем ее последние значения ключ значение
# в динамической таблицы по uuid объекта находим все записи о объекте
        # фильтруем по полям которые уже записаны
        # отсекаем их по последней дате
        # отсекаем значение и записываем их в словарь
"""
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


@background(schedule=60)
def find_actual_data(table_name, object_uuid, model, instance):
    # имя таблицы
    incoming_table_name = table_name
    # Получаем объект записи о динамической таблицы
    table_entry = RegisteredDynamicModel.objects.get(dynamic_model__exact=incoming_table_name)
    # Получаем token таблицы
    token_for_incoming_table = table_entry.token
    # Получаем все поля для данной таблицы
    all_entries_for_this_model = VariableNameModel.objects.filter(uuid_model__exact=token_for_incoming_table)
    # Лист для хранения имен полей таблицы
    var_name_list = []
    # Записывем в лист имен полей все названия полей
    for record in all_entries_for_this_model:
        var_name_list.append(record.name)
    # Получаем объект динамической таблицы
    schema_test = MyModel.objects.get(name=table_name)
    model_test = schema_test.as_model()
    # Словарь для для формировния
    object_to_send = {}
    # В цикле получаем все объекты таблицы
    # проверяем ее размер , если ноль не недаем ничего, но такого не может быть
    # в цикле по имени переменных и последней дате находим сортированной с конца
    # находим значения для этой переменной
    # записываем ее в словарь
    # после того как объект сформирован (вышли из цикла)
    # вызывем функцию по отправле http post запроса на mixer
    #
    for var in var_name_list:
        all_records = model_test.objects.all()
        if all_records.__len__() == 0:
            print("Empty")
        else:
            value = all_records.filter(object_uuid__exact=object_uuid
                                       ).filter(field__exact=var
                                                ).order_by('-changed')
            if value.__len__() == 0:
                current_value = "None"
            else:
                current_value = value[0].data.pop(var)

        object_to_send[var] = current_value
    send_data(object_uuid=object_uuid, recovered_object_data=object_to_send, model=model, instance=instance)


def send_data(object_uuid, recovered_object_data, model, instance):
    # это будет оправляться когда объекь будет готов к отправке
    # response = requests.request(
    #     method='POST',
    #     url='http://127.0.0.2:8080/restoring/test1/',
    #     data={
    #         "object": object_uuid,
    #         "model": model,
    #         "instance": instance,
    #         "data": recovered_object_data
    #     }
    # )
    # response.json()
    requests.post('http://127.0.0.2:8080/restoring/test1/', data={
        "object": object_uuid,
        "model": model,
        "instance": instance,
        "data": recovered_object_data
    })
