from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from .serializers import StudentSerializer
from .models import Student
from .utils import EmailThread
from django.conf import settings

# Create your views here.

loggers = logging.getLogger("mylogger")


@api_view(http_method_names=['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def studentView(request, format=None):
    if request.method == 'POST':
        try:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info('Student created successfully')
            user_email = request.user.email
            subject = 'Project Email'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                subject= subject,
                message= message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list=[user_email]
                ).start()
                return Response(data={'details: Email send Succesfully'})
            return Response(data=serializer.data, status=201)
        except:
            loggers.error("Error in creating a new student")
            return Response(data=serializer.errors,status=404)
        
    if  request.method == "GET":
        try:
            obj = Student.objects.all()
            serializer = StudentSerializer(obj, many=True)
            loggers.info('Student data fetched succesfully')
            return Response(data=serializer.data,status=200)
        except:
            loggers.error(data= serializer.errors, status=404)
            
@api_view(http_method_names=["PUT", "DELETE","PATCH","GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def details_api(request,pk):
    obj = get_object_or_404(Student,pk=pk)
    if request.method == "GET":
        try:
            serializer = StudentSerializer(obj)
            loggers.info('Student fetched succesfully')
            return  Response(data=serializer.data,status=200)
        except:
            loggers.error('Failed to retrieve the user information')
            return Response('Not found',status=404)
        
    if request.method == "PUT":
        try:
            serializer = StudentSerializer(data=request.data, instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info("Data updates")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'Updated Succesfully'
            if user_email:
                EmailThread(
                subject= subject,
                message= message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list=[user_email]
                ).start()
                return Response(data={'details: Email send Succesfully'})
            return Response(data=serializer.data,status=205)
        except:
            loggers.error("Updation  failed.")
            return Response(data=serializer.errors,status=400)
        
    if request.method == "PATCH":
        try:
            serializer = StudentSerializer(data=request.data, instance=obj, partial= True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info("Data updates")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'Updated Succesfully'
            if user_email:
                EmailThread(
                subject= subject,
                message= message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list=[user_email]
                ).start()
                return Response(data={'details: Email send Succesfully'})
            return Response(data=serializer.data,status=205)
        except:
            loggers.error("Updation  failed.")
            return Response(data=serializer.errors,status=400)
        
        
    if request.method=="DELETE":
        try:
            obj.delete()
            loggers.info("Deletion Successful")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'Deleted Succesfully'
            if user_email:
                EmailThread(
                subject= subject,
                message= message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list=[user_email]
                ).start()
                return Response(data={'details: Email send Succesfully'})
            return Response(data="Delete Succesfully", status=210)
        except:
            loggers.error("delete failed")
            return Response(data="error in delete", status=406)
