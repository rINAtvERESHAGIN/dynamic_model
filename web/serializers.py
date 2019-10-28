from rest_framework import serializers
from dynamo.models.models import MyModel

from dynamo.models.AllAction import AllAction
from dynamo.models.tree import Instance
from dynamo.models.RegisteredModels import RegisteredDynamicModel


class GetTableNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ('id',
                  '_modified',
                  'name')


class RegisteredModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredDynamicModel
        fields = (
            'id',
            'dynamic_model',
            'token',
            'instance',
            'model')


# BEGIN  нужны для формирования json который пойдет на фронт для tree view выбра таблицы
class InstanceSerializer(serializers.ModelSerializer):
    models = RegisteredModelSerializer(many=True, read_only=True)

    class Meta:
        model = Instance
        fields = (
            'id',
            'instance',
            'models')


"""
что такое generici 
views set 
router

nested_routers
"""


# END

class DynamicModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    field = serializers.CharField()
    data = serializers.CharField()
    previous = serializers.CharField()
    changed = serializers.DateTimeField()
    logged = serializers.DateTimeField()
    object_uuid = serializers.UUIDField()


class TestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    _modified = serializers.DateTimeField()
    name = serializers.CharField()


class AllActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    table_name = serializers.CharField()
    data = serializers.CharField()
    previous = serializers.CharField()
    action = serializers.CharField()


class CardsSerializer(serializers.Serializer):
    restored = serializers.IntegerField()
    logging = serializers.IntegerField()
    tables = serializers.IntegerField()
    changed = serializers.DateTimeField()
    type_of = serializers.CharField()
    data = serializers.CharField()
