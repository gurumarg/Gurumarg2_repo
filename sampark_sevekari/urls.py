from django.urls import path
from . import views

urlpatterns = [
     path('listof_SS_prashankarta',views.listof_SS_prashankarta,name='listof_SS_prashankarta'),
     path('listof_SS_rejected',views.listof_SS_rejected,name='listof_SS_rejected'),
     path('select_pp_question_seva',views.select_pp_question_seva,name='select_pp_question_seva'),
     path('view_seva_ss',views.view_seva_ss,name= 'view_seva_ss'),
     path('view_SS_selectedsevaid',views.view_SS_selectedsevaid,name='view_SS_selectedsevaid'),
     path('update_seva_ss',views.update_seva_ss,name='update_seva_ss'),
     path('pk_change_status',views.pk_change_status,name='pk_change_status'),
     path('change_status',views.change_status,name='change_status'),

]
