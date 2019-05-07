from django.db import models


class RegisteredDynamicModel(models.Model):
    model_name = models.CharField(max_length=100)
    token = models.UUIDField()


def registration(table_name, model_uuid):
    RegisteredDynamicModel.objects.create(model_name=table_name, token=model_uuid)
