from rest_framework.views import APIView
from dynamo.models.models import MyModel
from dynamo.models.AllAction import AllAction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from web.serializers import *


class Cards(APIView):
    def __init__(self, restored, logging, tables, changed, type_of, data):
        self.restored = restored
        self.logging = logging
        self.tables = tables
        self.changed = changed
        self.type_of = type_of
        self.data = data


def create_cards_object():
    count_table = MyModel.objects.all().__len__()  # сколько всего таблиц
    count_logging_object = AllAction.objects.all().__len__()  # сколько всего объектов залогинено
    count_object_restore = 5  # сколько всего объектов было восстановлено
    # TODO сделать проверку если 0 выскакивает исключение!
    last_object_logged = AllAction.objects.all().order_by('-id')[0]
    type_of = last_object_logged.action
    data = last_object_logged.data
    changed = last_object_logged.changed
    return Cards(count_object_restore, count_logging_object, count_table, changed, type_of, data)


@api_view(['GET', 'POST'])
def get_cards_info(request):
    if request.method == 'GET':
        cards = create_cards_object()
        serializer = CardsSerializer(cards)
        return Response(serializer.data)
