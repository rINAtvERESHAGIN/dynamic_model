from django.db import models

"""
Таблица которая хранит все действия по измененным данным
"""


class AllAction(models.Model):
    table_name = models.CharField(max_length=50)
    data = models.CharField(max_length=100)
    previous = models.CharField(max_length=100)
    action = models.CharField(max_length=20)
    changed = models.DateTimeField(auto_now=False, auto_now_add=False)



