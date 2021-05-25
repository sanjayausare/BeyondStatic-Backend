from .views import *
from django.urls import path, include

urlpatterns = [

    path('api/login', LoginAPI.as_view(), name='LoginAPI'),
    path('api/register', RegisterAPI.as_view(), name='RegisterAPI'),
    path('api/profile/<str:username>', ProfileAPI.as_view(), name='ProfileAPI'),
    path('api/<str:username>/project', ProjectAPI.as_view(), name='ProjectAPI'),
    path('api/project/<int:id>', ProjectInstanceAPI.as_view(), name='ProjectInstanceAPI'),
    path('api/addInstance/<str:message>', AddInstanceAPI.as_view(), name='AddInstanceAPI')
]