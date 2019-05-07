from django.db import models


class VariableNameModel(models.Model):
    name = models.CharField(max_length=50)
    uuid_model = models.UUIDField()  # Токен таблицы
