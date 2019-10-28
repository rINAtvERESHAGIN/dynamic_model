from django.db import models


# Create your models here.
class AllAction(models.Model):
    table_name = models.CharField(max_length=50)
    data = models.CharField(max_length=100)
    previous = models.CharField(max_length=100)
    action = models.CharField(max_length=20)
