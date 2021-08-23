from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from ..models import Dispatcher

@api_view(['GET', 'POST', 'PUT'])
def dispatcher_list(request):
    if request.method == "GET":
        try:
            dispatchers = Dispatcher.objects.all()
            serializer = DispatcherSerializer(dispatchers, many=True)
            data = {
                "success": True,
                "error": "",
                "data": serializer.data
            }
        except Exception as er:
            data = {
                "success": False,
                "error": "{}".format(er),
                "message": "Dispatchers are not found!"
            }
        return Response(data)

    elif request.method == "POST":
        try:
            serializer = DispatcherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "success": True,
                    "error": "",
                    "message": "Dispatcher created successfully",
                    "data": serializer.data
                }
        except Exception as er:
            data = {
                "success": False,
                "error": "{}".format(er),
                "message": "Dispatcher not created!"
            }
        return Response(data)

