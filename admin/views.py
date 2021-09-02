from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth import get_user_model

from common.models import session_data,seva_data
from common.views import modify_user_type
from django.contrib import messages

User = get_user_model()

# Create your views here.


def users_page(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    return render(request, 'users_page.html',{'user_details': user_details})

# function ss_data will show list of current sampark sevekari

def ss_data(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    ss_table = get_user_model().objects.filter(type='sampark_sevekari')
    function1 = 'sst'
    return render(request, 'users_page.html', {'user_details':user_details,'ss_table': ss_table,'function1':function1})

def add_ss(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    ss_table = get_user_model().objects.filter(type='verified')
    function2 = 'ass'
    return render(request, 'users_page.html', {'user_details':user_details,'ss_table': ss_table,'function2':function2})


def edit_ss_data(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    modify_user_type(request)
    return render(request,'users_page.html',{'user_details':user_details})

def listof_main_admin(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    allmain_admins = get_user_model().objects.filter(type='main_admin')
    function3 = 'listof_main_admins'
    return render(request,'users_page.html',{'user_details':user_details,'function3':function3,'data':allmain_admins})

def listof_prashankarta(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    all_prashankarta = get_user_model().objects.filter(type='verified')
    function4 = 'listof_prashankarta'
    return render(request,'users_page.html',{'user_details':user_details,'function4':function4,'data':all_prashankarta})

def listof_rejected(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    all_rejected = get_user_model().objects.filter(type='rejected')
    function5 = 'listof_rejected'
    return render(request,'users_page.html',{'user_details':user_details,'function5':function5,'data':all_rejected})

def listof_unverified(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    all_unverified = get_user_model().objects.filter(type='unverified')
    function6 = 'listof_unverified'
    return render(request,'users_page.html',{'user_details':user_details,'function6':function6,'data':all_unverified})

def select_pk_seva(request):
    id = request.POST['user']
    x = request.POST['x']
    user_details = get_user_model().objects.get(pk=id)

    userlist=[]
    if x == 'schedule':
        pk_table = session_data.objects.filter(status='submitted')
        function2 = 'ud1'
    elif x== 'viewseva':
        pk_table = session_data.objects.filter(status='completed')
        function2 = 'udview'
    else:
        pk_table = session_data.objects.filter(status='scheduled')
        function2 = 'schedule_data'
    userlist = createlist(pk_table)

    return render(request, 'Home_admin.html', {'user_details': user_details,'userlist': userlist ,'function2':function2})

def prashan_schedule(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    session_id = request.POST['select_questions']
    record = session_data.objects.get(pk=session_id)
    pkdata = get_user_model().objects.get(id=record.User_id_id)
    userlist = []
    function2 = 'ud1'
    if pkdata.type == 'unverified':
        messages.info(request,' ❗ सिलेक्ट केलेला प्रश्नकर्ता वेरिफाइड नाही आहे ❗ ')
    else:
        record.status='scheduled'
        record.save()
        messages.info(request,'👍 सेशन आइडी'+'  ' + session_id + ' शेड्युल  यशस्वी 👍')
    pk_table = session_data.objects.filter(status='submitted')
    userlist = createlist(pk_table)

    return render(request, 'Home_admin.html', {'user_details': user_details,'userlist': userlist ,'function2':function2})


def createlist(pk_table):
    pk_table = pk_table
    userlist = []
    for i in pk_table:
        id=i.User_id
        session_id=i.session_id
        prashan1=i.prashan1
        prashan2 = i.prashan2
        Date_filled = i.Date_filled
        userdata = get_user_model().objects.get(mobile1=id)
        full_name = (userdata.first_name)+ ' ' + (userdata.last_name)
        mobile1=userdata.mobile1
        mobile2=userdata.mobile2
        user_id=userdata.id
        city=userdata.city

        dic1={'user_id':user_id,'session_id':session_id,'prashan1':prashan1,'prashan2':prashan2,
               'Date_filled':Date_filled,'city':city,'full_name':full_name,'mobile1':mobile1,'mobile2':mobile2}

        userlist.append(dic1)
    return userlist


def load_sevaform(request):
    session_id = request.POST['select_name']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    userdata=session_data.objects.get(pk=session_id)
    prashan1 = userdata.prashan1
    prashan2 = userdata.prashan2
    pid = userdata.User_id_id
    udata = get_user_model().objects.get(pk=pid)
    full_name = udata.first_name + ' ' + udata.last_name
    email = udata.email
    previous_seva = seva_data.objects.filter(session_id=session_id)
    print('previous_seva:', previous_seva)
    dic1 = {'full_name':full_name,'prashan1':prashan1,'prashan2':prashan2,'session_id':session_id,'pid':pid,'email':email}
    return render(request,'sevaform.html',{'user_details':user_details,'previous_seva': previous_seva,'dic1':dic1})


def save_seva(request):
    pitraseva = request.POST.getlist('pitraseva')
    maansanam = request.POST.getlist('maansanam')
    mantrajaap = request.POST.getlist('mantrajaap')
    parayaan = request.POST.getlist('parayaan')
    strotatvachan = request.POST.getlist('strotatvachan')
    yantrastapana = request.POST.getlist('yantrastapana')
    sukt = request.POST.getlist('sukt')
    otherseva = request.POST.getlist('otherseva')
    vishesh_suchana_seva = request.POST.getlist('vishesh_suchana_seva')
    guru_ans_p1= request.POST['guru_ans_p1']
    guru_ans_p2 = request.POST['guru_ans_p2']

    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    session_id = request.POST['session_id']
    pid = request.POST['pid']
    email=request.POST['email']
    print('email is ',email)
    list = [pitraseva, maansanam, mantrajaap, parayaan, strotatvachan, yantrastapana, sukt, otherseva,
            vishesh_suchana_seva]
    sevalist=[]
    pending_seva=[]
    seva16 = ' '

    for i in list:
        for j in i:
            if len(sevalist)<=14:
                sevalist.append(j)
            else:
                pending_seva.append(j)
                seva16 = seva16 + ' ,\n ' + j
    x=len(sevalist)
    while x < 14:
        sevalist.append(' ')
        x=x+1

    seva1 = sevalist[0]
    seva2 = sevalist[1]
    seva3 = sevalist[2]
    seva4 = sevalist[3]
    seva5 = sevalist[4]
    seva6 = sevalist[5]
    seva7 = sevalist[6]
    seva8 = sevalist[7]
    seva9 = sevalist[8]
    seva10 = sevalist[9]
    seva11 = sevalist[10]
    seva12 = sevalist[11]
    seva13 = sevalist[12]
    seva14 = sevalist[13]
    if len(pending_seva) == 0:
        seva15 = 0
    else:
        seva15 = pending_seva

    newseva = seva_data(seva1=seva1,seva2=seva2,seva3=seva3,seva4=seva4,seva5=seva5,seva6=seva6,seva7=seva7,
                        seva8=seva8,seva9=seva9,seva10=seva10,seva11=seva11,seva12=seva12,seva13=seva13,seva14=seva14,
                        seva15=seva15,session_id_id=session_id,user_id_id=pid,guru_ans_p1=guru_ans_p1,guru_ans_p2=guru_ans_p2)
    newseva.save()

    record = session_data.objects.get(pk=session_id)
    record.status='completed'
    record.save()

    msg = 'रोजची नित्य उपासना'+ '\n' +'मंत्र जप:'+ '\n' + ' 1. || श्री गुरु स्वामी समर्थ जय जय स्वामी समर्थ || * ११ वेळा * '+ \
          '\n' +'2.|| श्री स्वामी समर्थ || * 3 माळ *'+ '\n' +'3. ||  शिव चिदंबर || * १ माळ *'+ '\n' +'पोथी वाचन:' +\
          '\n' + '1. स्वामी चरित्र सारामृत ( रोज १ किंवा ३ अध्याय )'+ \
          '\n' + 'पोथी वाचन  क्रम : ( दिवस १ : अध्याय १ , दिवस २ : अध्याय २,.....)   किंवा ( दिवस १: अध्याय १,२,३ ,   दिवस २ : अध्याय ४,५,६,   ....)'+\
          '\n' +' 2. दुर्गासप्तशती ( रोज २ अध्याय वाचन )' + '\n' + 'पोथी वाचन  क्रम : ( दिवस १: अध्याय १,२  ,  दिवस २ : अध्याय ,३,४   ,  ....) '+\
          '\n' + 'नैवैद्य: रोज सकाळ संध्याकाळ महाराजांना नैवैद्य दाखविणे '+ '\n' +  seva1 + \
          '\n' + seva2 +'\n' + seva3 + '\n' + seva4 + \
          '\n' + seva5 + '\n' + seva6 + '\n' + seva7 + '\n'+seva8 + '\n' + seva9 + '\n' + seva10 + '\n' + seva11 + \
          '\n' + seva12 + '\n' + seva13 + '\n' + seva14 + '\n' + seva16
    send_mail('दिलेली सेवा ', msg, 'samarthview@gmail.com',
              [email, 'gurumargdarshan14@gmail.com'], fail_silently=True)



    function2 = 'ds'
    return render(request, 'Home_admin.html',
                  {'user_details': user_details, 'display_seva': sevalist, 'pending_list':pending_seva, 'function2': function2})


