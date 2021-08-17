from django.urls import path
from . import views

urlpatterns = [


      path('registration_check',views.registration_check,name='registration_check'),


]
