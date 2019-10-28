from django.shortcuts import render
from rest_framework.views import APIView
from dynamo.models.models import MyModel
from web.serializers import GetTableNameSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from dynamo.models.AllAction import AllAction
from web.serializers import *


# Create your views here.
@api_view(['GET', 'POST'])
def get_all_action(request):
    if request.method == 'GET':
        all_action = AllAction.objects.all()
        serializer = AllActionSerializer(all_action, many='True')
        return Response(serializer.data)
