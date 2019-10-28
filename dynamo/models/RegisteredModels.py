from django.db import models
from dynamo.models.tree import Instance

"""Регестрация новой таблицы"""


class RegisteredDynamicModel(models.Model):
    dynamic_model = models.CharField(max_length=100)
    token = models.UUIDField()
    model = models.CharField(max_length=100, null=True)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, null=True, related_name='models')


def registration(table_name, model_uuid):
    RegisteredDynamicModel.objects.create(model_name=table_name, token=model_uuid)
