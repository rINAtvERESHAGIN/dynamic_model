from django.db import models


class Instance(models.Model):
    instance = models.CharField(max_length=100)
