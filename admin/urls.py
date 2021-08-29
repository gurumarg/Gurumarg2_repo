from django.urls import path
from . import views

urlpatterns = [
     path('users_page',views.users_page,name='users_page'),
     path('ss_data',views.ss_data,name='ss_data'),
     path('add_ss',views.add_ss,name = 'add_ss'),
     path('edit_ss_data',views.edit_ss_data,name='edit_ss_data'),
     path('listof_main_admin',views.listof_main_admin,name='listof_main_admin'),

]
