from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
from rest_framework.views import APIView
from dynamo.models import *
from rest_framework.response import Response
from rest_framework import status
from dynamo.serializers import *
import datetime
from django.conf import settings
import uuid
from dynamo.models.VariableNamesModel import VariableNameModel
from dynamo.models.RegisteredModels import RegisteredDynamicModel
from dynamo.serializers import RestoringObjectSerializer

"""
1. Происходит выбор значения которое нужно восстановить
2. Посылается table_name , object_uuid

"""


class WebAppRestoring(APIView):
    pass
