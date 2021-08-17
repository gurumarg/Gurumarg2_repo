from django.urls import path
from . import views

urlpatterns = [

      path('',views.homepage,name='home'),
      path('annadan',views.annadanpage,name='annadan'),
      path('sahitya',views.sahityapage,name='sahitya'),
      path('loginpage',views.loginpage,name='loginpage'),
      path('registerpage',views.registerpage,name='registerpage'),
      path('register',views.register,name='register'),
      path('send_email',views.send_email,name='send_email'),
      path('verify_ecode',views.verify_ecode,name='verify_ecode'),



]
