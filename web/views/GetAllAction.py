from web.serializers import *
from rest_framework.views import APIView
from dynamo.models.AllAction import AllAction

from rest_framework.response import Response


class AllActionData(APIView):
    modal_data = ''

    def get(self, request):
        self.modal_data = AllAction.objects.get()
        serializer = AllActionSerializer(self.modal_data, many='True')
        return Response(serializer.data)
