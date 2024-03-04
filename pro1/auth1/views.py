from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
import logging

# Create your views here.

loggers = logging.getLogger('mylogger')


@api_view(http_method_names=([ 'POST']))
def user(request):
    if request.method == "POST":
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info('Student created succesfully')
            return Response(data=serializer.data, status=201)
        except:
            loggers.error("Error in creating a new student")
            return Response(data=serializer.errors,status=404)