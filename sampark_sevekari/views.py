from django.shortcuts import render
from django.contrib.auth import get_user_model
from common.models import sampark_sevekari,session_data,seva_data
from django.contrib import messages

from common.views import prashandetails, make_seva_dic

User = get_user_model()

# Create your views here.
def listof_SS_prashankarta(request):
    button_clicked = request.POST['b1']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    record = sampark_sevekari.objects.get(User_id_id = id)
    sscode = record.sscode
    all_prashankarta = get_user_model().objects.filter(sscode=sscode)
    function1 = 'listof_SS_prashankarta'
    if button_clicked == 'prashnakarta':
        x = 'prashnakarta'
    elif button_clicked == 'prashnakarta_seva':
        x = 'prashnakarta_seva'
    elif button_clicked == 'tumche_pk':
        x = 'tumche_pk'
    else:
        x = ''
    if user_details.type == 'sampark_sevekari':
         return render(request,'home_sampark_sevekari.html',{'user_details':user_details,
                                'function1':function1,'data':all_prashankarta,'x':x})

    elif user_details.type == 'main_admin':
        return render(request, 'users_page.html', {'user_details': user_details,
                                  'function1': function1, 'data': all_prashankarta, 'x': x})

def listof_SS_rejected(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    record = sampark_sevekari.objects.get(User_id_id = id)
    sscode = record.sscode
    all_prashankarta = get_user_model().objects.filter(sscode=sscode).filter(type='Rejected')
    function1 = 'listof_SS_prashankarta'
    return render(request,'home_sampark_sevekari.html',{'user_details':user_details,'function1':function1,'data':all_prashankarta})


def select_pp_question_seva(request):
    pk_id = int(request.POST['select_name'])
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    pk_table = session_data.objects.filter(User_id_id = pk_id)
    function2 = 'display questions'
    if user_details.type == 'sampark_sevekari':
            return render(request,'home_sampark_sevekari.html',{'user_details':user_details,'pk_table':pk_table, 'function2':function2})
    elif user_details.type == 'main_admin':
            return render(request,'users_page.html',{'user_details':user_details,'pk_table':pk_table, 'function2':function2})

def view_seva_ss(request):
    session_id = request.POST['select_session_id']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    dic1 = prashandetails(session_id)
    sevadetails = seva_data.objects.filter(session_id_id=session_id)
    sevadic = sevadetails
    i = 0
    for x in sevadetails:
        i += 1
    if i == 0:
        function2 = ''
        messages.info(request,'निवडलेल्या प्रश्नाकरिता सेवा दिलेली नाही ')
    elif i == 1:
        function2 = 'user_seva_display'
        sevadetails = seva_data.objects.get(session_id_id=session_id)
        sevadic = make_seva_dic(sevadetails)
        print('SS sevadic', sevadic)
    else:
        function2 = 'multiple_seva_id'
    if user_details.type == 'samapark_sevekari':

         return render(request, 'home_sampark_sevekari.html',{'user_details': user_details,'dic1':dic1,'sd':sevadic,'function2': function2,'session_id':session_id})

    elif user_details.type == 'main_admin':
        return render(request, 'users_page.html',{'user_details': user_details, 'dic1': dic1, 'sd': sevadic, 'function2': function2,'session_id': session_id})


def view_SS_selectedsevaid(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    seva_id = request.POST['seva_id']
    session_id = request.POST['session_id']
    dic1 = prashandetails(session_id)
    sevadetails = seva_data.objects.get(seva_id = seva_id)
    sevadic = make_seva_dic(sevadetails)
    print('sevadic return value',sevadic)
    function2 = 'user_seva_display'
    if user_details.type == 'sampark_sevekari':
         return render(request, 'home_sampark_sevekari.html',
                  {'user_details': user_details, 'dic1': dic1, 'sd': sevadic, 'function2': function2})
    elif user_details.type == 'main_admin':
        return render(request, 'users_page.html',
                      {'user_details': user_details, 'dic1': dic1, 'sd': sevadic, 'function2': function2})


def update_seva_ss(request):
    seva_expalined = request.POST['seva_expalined']
    seva_id = request.POST['seva_id']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    record = seva_data.objects.get(pk = seva_id)
    record.seva_explained = seva_expalined
    record.save()
    messages.info(request, ' ✅ सेवा अपडेटेड कम्प्लिटेड  ✅ ')
    type = user_details.type
    if type == 'sampark_sevekari':
        return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
    elif type == 'main_admin':
        return render(request, 'users_page.html', {'user_details': user_details})




