from django.urls import path
from .views import studentView , details_api

urlpatterns = [
    path('add/',studentView),
    path('add/<int:pk>/',details_api),
]