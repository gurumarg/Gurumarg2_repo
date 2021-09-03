from django.urls import path
from . import views

urlpatterns = [
     path('users_page',views.users_page,name='users_page'),
     path('ss_data',views.ss_data,name='ss_data'),
     path('add_ss',views.add_ss,name = 'add_ss'),
     path('edit_ss_data',views.edit_ss_data,name='edit_ss_data'),
     path('listof_main_admin',views.listof_main_admin,name='listof_main_admin'),
     path('listof_prashankarta',views.listof_prashankarta,name='listof_prashankarta'),
     path('listof_rejected', views.listof_rejected, name='listof_rejected'),
     path('listof_unverified', views.listof_unverified, name='listof_unverified'),
     path('select_pk_seva', views.select_pk_seva, name='select_pk_seva'),
     path('prashan_schedule', views.prashan_schedule, name='prashan_schedule'),
     path('load_sevaform',views.load_sevaform,name='load_sevaform'),
     path('save_seva',views.save_seva,name='save_seva'),



]
