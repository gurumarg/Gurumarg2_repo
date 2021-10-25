from django.urls import path
from . import views

urlpatterns = [

      path('',views.homepage,name='home'),
      path('m_home',views.homepage,name='m_home'),
      path('annadan',views.annadanpage,name='annadan'),
      path('sahitya',views.sahityapage,name='sahitya'),
      path('loginpage',views.loginpage,name='loginpage'),
      path('registerpage',views.registerpage,name='registerpage'),
      path('register',views.register,name='register'),
      path('send_email',views.send_email,name='send_email'),
      path('verify_ecode',views.verify_ecode,name='verify_ecode'),
      path('registration_check',views.registration_check,name='registration_check'),
      path('applogin',views.applogin,name='applogin'),
      path('logout',views.userlogout,name='logout'),
      path('returntohome',views.returntohome,name='returntohome'),
      path('forgot_password', views.forgot_password,name='forgot_password'),
      path('fp_verify_code', views.fp_verify_code, name='fp_verify_code'),
      path('fp_check_password',views.fp_check_password,name='fp_check_password'),

]
