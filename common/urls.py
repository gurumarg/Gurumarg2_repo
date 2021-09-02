from django.urls import path
from . import views

urlpatterns = [
     path('question_form',views.question_form,name='question_form'),
     path('return_to_home',views.return_to_home,name='return_to_home'),
     path('save_prashan',views.save_prashan,name='save_prashan'),
     path('profile_manage',views.profile_manage,name='profile_manage'),
     path('profile_update',views.profile_update,name='profile_update'),
     path('verify_recode',views.verify_recode,name='verify_recode'),
     path('approve_kara',views.approve_kara, name='approve_kara'),
     path('modify_user_type',views.modify_user_type,name='modify_user_type'),
     path('new_question',views.new_question,name='new_question'),
     path('repeat_question',views.repeat_question,name='repeat_question'),
     path('submit_repeat_question',views.submit_repeat_question,name='submit_repeat_question'),
     path('select_question_seva',views.select_question_seva,name='select_question_seva'),
     path('view_seva',views.view_seva,name='view_seva'),
     path('view_selectedsevaid',views.view_selectedsevaid,name = 'view_selectedsevaid'),
     path('update_seva',views.update_seva,name='update_seva'),

]
