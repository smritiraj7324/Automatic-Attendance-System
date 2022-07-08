from django.urls import path
from . import views
urlpatterns = [ 
    path('take_attend/',views.startCameraForAttendance, name = 'take_attend')
]