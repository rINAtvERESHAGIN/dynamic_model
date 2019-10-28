from background_task import background
from dynamo.views.common_classes.logging_object import LoggingObject

# test fun check_by_object_uuid
previous_to_return = ''


@background(schedule=10)
def start_log(json_data, table_name):
    logging_object = LoggingObject(json_data, table_name)
    logging_object.get_incoming_data()

    if logging_object.check_by_object_uuid():
        logging_object.previous = None
    else:
        if logging_object.check_by_changed():
            print('Хронология восстановлена')
        else:
            print('Хронология не нарушина')
            logging_object.previous = logging_object.find_previous()
    print('начал делать новый!')
    logging_object.object_formation()
    logging_object.mark_action(table_name)
