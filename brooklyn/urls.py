from .views import *
from django.urls import path, include

urlpatterns = [
    path('api/tokencheck', TokenCheckAPI.as_view(), name='TokenCheckAPI'),
    path('api/login', LoginAPI.as_view(), name='LoginAPI'),
    path('api/register', RegisterAPI.as_view(), name='RegisterAPI'),
    path('api/profile/<str:username>', ProfileAPI.as_view(), name='ProfileAPI'),
    path('api/<str:username>/project', ProjectAPI.as_view(), name='ProjectAPI'),
    path('api/project/<int:id>', ProjectInstanceAPI.as_view(), name='ProjectInstanceAPI'),
    path('api/addInstance/<str:message>', AddInstanceAPI.as_view(), name='AddInstanceAPI'),
    path('api/projectobjects/<int:projectID>', ProjectObjectsAPI.as_view(), name='ProjectObjectsAPI'),
    path('api/projectobject/<int:projectobjectID>', ProjectObjectAPI.as_view(), name='ProjectObjectAPI'),
    path('api/allmessagescount/<str:username>', AllMessagesCountAPI.as_view(), name='AllMessagesCountAPI'),
    path('api/chartdata/<str:username>', ChartDataAPI.as_view(), name='ChartDataAPI'),
    path('api/projectchartdata/<str:username>/<int:projectID>', ProjectChartDataAPI.as_view(), name="ProjectChartDataAPI"),
    path('api/lastdaymessagescount/<str:username>', LastDayMessagesCountAPI.as_view(), name="LastDayMessagesCountAPI")
]