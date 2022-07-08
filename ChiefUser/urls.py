from django.urls import path
from . import views 

urlpatterns = [
    path('admin_panel/',views.admin_panel, name = "admin_panel"),  #after admin successful admin-login
    path('admin_login/',views.admin_login,name="admin_login"),
    path('addNew/',views.addANewEmp, name = 'addNew'),
    path('faceSample/',views.takeFaceSample, name = 'FaceSample'),  # a..dance after movement on this page
    path('faceSamplepg/',views.faceSamplePage, name = 'FaceSamplepg')  # movement on page..a
]