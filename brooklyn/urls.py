from .views import *
from django.urls import path, include

urlpatterns = [

    path('api/login', LoginAPI.as_view(), name='LoginAPI'),
    path('api/register', RegisterAPI.as_view(), name='RegisterAPI'),
    path('api/profile/<str:username>', ProfileAPI.as_view(), name='ProfileAPI'),
    
]