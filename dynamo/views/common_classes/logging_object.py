import datetime
import uuid
from dynamo.models.models import MyModel
from dynamo.models.AllAction import AllAction


class LoggingObject:
    table_schema = ''
    # data_dict = ''

    object_uuid = ''
    changed = ''
    data = ''
    previous = ''
    field = ''
    record_uuid = ''
    type_of = ''

    def __init__(self, data_dict, table_name):
        self.data_dict = data_dict
        self.table_name = table_name

    def find_previous(self):
        # получаем актуальные данные которые будут предыдущими для нового объекта.
        number_of_field = self.table_schema.objects.filter(field__exact=self.field)
        if number_of_field.__len__() > 0:
            try:
                object_on_uuid = self.table_schema.objects.filter(object_uuid__exact=self.object_uuid
                                                                  ).filter(field__exact=self.field
                                                                           ).order_by('-changed')[0]
                previous = object_on_uuid.record_uuid
            except Exception:
                print("What!")
            return previous
        else:
            return None

    def check_by_changed(self):
        """
            check_by_changed - функция задача которой является :
            Проверка по времени ( если происходят задержки на сервере)
            """
        """
        Находим все записи об этом объекте по его uuid
        Находим записи по конкретному полю ( var )
        """
        all_found = self.table_schema.objects.filter(object_uuid__exact=self.object_uuid
                                                     ).filter(field__exact=self.field
                                                              ).order_by('id')
        # TODO доработка принятия времени - время изменения только что пришедшего объекта
        changed_time = datetime.datetime.strptime(self.changed, '%Y-%m-%d')
        flag = False
        """
                # если время изменения какого-то записанного объекта больше
                # чем время изменения объекта который пришел только  то =>
                # записываем значения существующего объекта в новую ссылку
                # предыдущая запись спешащего объекта
                # сохранненому объекту ( который старше по времени ) меняет previous на данные входящего
                # входящему объекту ставим previous который был автоматически поставлен сохраненному объекту
        """
        for record in all_found:
            if record.changed > changed_time:
                hurried_object = record
                hurried_object_previous = hurried_object.previous
                print(hurried_object_previous)
                find_object = self.table_schema.objects.filter(record_uuid__exact=hurried_object_previous)
                if find_object.__len__() == 0:
                    print('Нет тут ничего')
                else:
                    print(find_object[0].data)

                self.table_schema.objects.filter(pk=hurried_object.id).update(previous=self.record_uuid)
                self.previous = hurried_object_previous
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

    def check_by_object_uuid(self):
        # получаем все записи в объекте
        objects = self.table_schema.objects.filter(object_uuid__exact=self.object_uuid)
        if objects.__len__() == 0:
            print('Да такого еще не было')
            return True
        else:
            print('Такой уже есть смотрим дальше')
            return False

    def object_formation(self):
        self.table_schema.objects.create(data=self.data,  # json # data for log
                                         field=self.field,
                                         logged=datetime.datetime.now(),  # time when log is writen
                                         type_of=self.type_of,  # json  # type of signal
                                         object_uuid=self.object_uuid,
                                         # json  # object uuid that come from instance
                                         changed=self.changed,  # json  # time when object changed in front
                                         record_uuid=self.record_uuid,  # my own uuid
                                         previous=self.previous,
                                         )

    def get_incoming_data(self):
        model_schema = MyModel.objects.get(name=self.table_name)
        self.table_schema = model_schema.as_model()
        # from json
        self.data = self.data_dict.pop('data')
        print(self.data)
        self.type_of = self.data_dict.pop('type_of')
        self.object_uuid = self.data_dict.pop('object_uuid')
        self.changed = self.data_dict.pop('changed')

        self.set_and_parse_json_key()
        self.record_uuid = uuid.uuid4()

        print('self.type_of - work ', self.type_of)

    """
    метод mark_action формирует и сохраняет объект в таблицу AllAction - для фронта!
    """

    def mark_action(self, table_name):
        print('')
        if self.previous is None:
            previous = 'None'
        else:
            previous_data = self.table_schema.objects.get(record_uuid=self.previous)
            previous = previous_data.data.pop(self.field)
        data_a = self.data.pop(self.field)

        AllAction.objects.create(table_name=table_name,
                                 data=data_a,
                                 previous=previous,
                                 action=self.type_of,
                                 changed=self.changed)
