from django.urls import path
from . import views

urlpatterns = [
     path('users_page',views.users_page,name='users_page'),


]
