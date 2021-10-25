"""Gurumarg2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('question_form',include('common.urls')),
    path('users_page',include('admin.urls')),
    path('listof_SS_prashankarta',include('sampark_sevekari.urls')),
    path('show_selectedseva',include('admin.urls')),
    path('users_page', include('admin.urls')),
    path('ss_data', include('admin.urls')),
    path('add_ss', include('admin.urls')),
    path('edit_ss_data', include('admin.urls')),
    path('listof_main_admin', include('admin.urls')),
    path('listof_prashankarta', include('admin.urls')),
    path('listof_rejected', include('admin.urls')),
    path('listof_unverified', include('admin.urls')),
    path('select_pk_seva', include('admin.urls')),
    path('prashan_schedule', include('admin.urls')),
    path('load_sevaform', include('admin.urls')),
    path('save_seva', include('admin.urls')),
    path('show_selectedseva', include('admin.urls')),
    path('return_to_home',include('common.urls')),
    path('save_prashan',include('common.urls')),
    path('profile_manage',include('common.urls')),
    path('profile_update',include('common.urls')),
    path('verify_recode',include('common.urls')),
    path('approve_kara',include('common.urls')),
    path('modify_user_type',include('common.urls')),
    path('new_question',include('common.urls')),
    path('repeat_question',include('common.urls')),
    path('submit_repeat_question',include('common.urls')),
    path('select_question_seva',include('common.urls')),
    path('view_seva',include('common.urls')),
    path('view_selectedsevaid',include('common.urls')),
    path('update_seva',include('common.urls')),
    path('annadan',include('home.urls')),
    path('sahitya',include('home.urls')),
    path('loginpage',include('home.urls')),
    path('registerpage',include('home.urls')),
    path('register',include('home.urls')),
    path('send_email',include('home.urls')),
    path('verify_ecode',include('home.urls')),
    path('registration_check',include('home.urls')),
    path('applogin',include('home.urls')),
    path('forgot_password',include('home.urls')),
    path('logout',include('home.urls')),
    path('returntohome',include('home.urls')),
    path('update_seva_ss', include('sampark_sevekari.urls')),
    path('listof_SS_rejected', include('sampark_sevekari.urls')),
    path('select_pp_question_seva', include('sampark_sevekari.urls')),
    path('view_seva_ss', include('sampark_sevekari.urls')),
    path('view_SS_selectedsevaid', include('sampark_sevekari.urls')),
    path('fp_verify_code', include('home.urls')),
    path('fp_check_password',include('home.urls')),


]
