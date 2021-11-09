from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from common.models import session_data, seva_data, st_data, sampark_sevekari
from common.views import modify_user_type
from django.contrib import messages
from datetime import date

User = get_user_model()

# Create your views here.
# show_timeslots will fetch time slots avaiable on date selected by admin

def show_timeslots(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    schedule_date = request.POST['schedule_date']
    session_id = request.POST['select_questions']
    booked_timeslots = session_data.objects.filter(schedule_date = schedule_date).values('schedule_time')

    timeslots = {'7:00AM': 'open', '7:15AM': 'open', '7:30AM': 'open', '8:00AM': 'open', '8:30AM':'open',
                 '8:45AM': 'open', '9:00AM': 'open', '9:15AM': 'open', '9:30AM': 'open', '9:45AM':'open',
                 '10:00AM': 'open', '10:15AM': 'open', '10:30AM': 'open', '10:45AM':'open',
                 '11:00AM': 'open', '11:15AM': 'open', '11:30AM': 'open', '11:45AM':'open',
                 '12:00PM': 'open', '12:15PM': 'open', '12:30PM': 'open', '12:45PM': 'open',
                 '01:00PM': 'open', '01:15PM': 'open', '01:30PM': 'open', '01:45PM': 'open',
                 '02:00PM': 'open', '02:15PM': 'open', '02:30PM': 'open', '02:45PM': 'open',
                 '03:00PM': 'open', '03:15PM': 'open', '03:30PM': 'open', '03:45PM': 'open',
                 '04:00PM': 'open', '04:15PM': 'open', '04:30PM': 'open', '04:45PM': 'open',
                 '05:00PM': 'open', '05:15PM': 'open', '05:30PM': 'open', '05:45PM': 'open',
                 '06:00PM': 'open', '06:15PM': 'open', '06:30PM': 'open', '06:45PM': 'open',
                 '07:00PM': 'open', '07:15PM': 'open', '07:30PM': 'open', '07:45PM': 'open',
                 '08:00PM': 'open', '08:15PM': 'open', '08:30PM': 'open', '08:45PM': 'open',
                 '09:00PM': 'open', '09:15PM': 'open', '09:30PM': 'open', '09:45PM': 'open',
                 }
    list_bookedslots = list(booked_timeslots)
    if list_bookedslots:
        for x in list_bookedslots:
          y = x['schedule_time']
          timeslots[y] = 'booked'
        status = 'booked'
        for i in timeslots:
             if timeslots[i] == 'open':
                status = 'available'
                break
        if status == 'booked':
            messages.info(request,'सर्व स्लॉट्स बुक आहेत , कृपया नवीन तारीख निवडावी ')
            return render(request,'home_admin.html',{'user_details': user_details})

    return render(request,'home_admin.html',{'timeslots':timeslots,'user_details': user_details,
                                             'function2':'timeslot','session_id':session_id,'schedule_date':schedule_date})

def users_page(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    return render(request, 'users_page.html',{'user_details': user_details})


# function ss_data will show list of current sampark sevekari

def ss_data(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    ss_table = get_user_model().objects.filter(type='sampark_sevekari')
    if not ss_table:
        messages.info(request,"सध्या संपर्क सेवेकरी म्हणून कुणालाही निवडलेले नाही ")
        return render(request, 'users_page.html', {'user_details': user_details})
    else:
        function1 = 'sst'
        return render(request, 'users_page.html', {'user_details':user_details,'ss_table': ss_table,'function1':function1})

def add_ss(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    ss_table = get_user_model().objects.filter(type='verified')
    if not ss_table:
        messages.info(request," वेरिफाइड युजर नाही ")
        return render(request, 'users_page.html', {'user_details': user_details})
    else:
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
    if not allmain_admins:
        messages.info(request, " सध्या कोणीही मेंन ऍडमीन नाही  ")
        return render(request, 'users_page.html', {'user_details': user_details})
    else:
        function3 = 'listof_main_admins'
        return render(request,'users_page.html',{'user_details':user_details,'function3':function3,'data':allmain_admins})

def listof_prashankarta(request):
    buttonclicked = request.POST['b3']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    all_prashankarta = get_user_model().objects.exclude(type='Rejected').exclude(type='unverified')
    if not all_prashankarta:
        messages.info(request, " सध्या प्रश्नकर्ता नाही ")
        return render(request, 'users_page.html', {'user_details': user_details})
    else:
        function4 = 'listof_prashankarta'
        return render(request,'users_page.html',{'user_details':user_details,'function4':function4,
                                                 'data':all_prashankarta,'buttonclicked':buttonclicked})

def listof_rejected(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    all_rejected = get_user_model().objects.filter(type='Rejected')
    if not all_rejected:
        messages.info(request, " सध्या कोणीही रीजेक्टेड प्रश्नकर्ता नाही ")
        return render(request, 'users_page.html', {'user_details': user_details})
    else:
        function5 = 'listof_rejected'
        return render(request,'users_page.html',{'user_details':user_details,'function5':function5,'data':all_rejected})

def listof_unverified(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    all_unverified = get_user_model().objects.filter(type='unverified')
    if not all_unverified:
        messages.info(request, " सध्या कोणीही अनवेरिफाइड प्रश्नकर्ता नाही ")
        return render(request, 'users_page.html', {'user_details': user_details})
    else:
        function6 = 'listof_unverified'
        return render(request,'users_page.html',{'user_details':user_details,'function6':function6,'data':all_unverified})

def select_pk_seva(request):
    id = request.POST['user']
    x = request.POST['x']
    user_details = get_user_model().objects.get(pk=id)

    userlist=[]
    if x == 'schedule':
        pk_table = session_data.objects.exclude(status='completed').exclude(status='rejected').exclude(status='scheduled')
        function2 = 'ud1'
    elif x== 'viewseva':
        pk_table = session_data.objects.filter(status='completed')
        function2 = 'udview'
    elif x == 'start session':
        today = date.today()
        pk_table = session_data.objects.filter(schedule_date=today)
        if pk_table:
            try:
                st_update = st_data.objects.get(st_date=today)
                st_update.st_status = 'start'
                st_update.save()
            except:
                new_session = st_data(st_date=today,st_status='start')
                new_session.save()
            function2 = 'schedule_data'
        else:
            messages.info(request,'आज प्रश्नोत्तरे नाही आहे ')
            return render(request,'home_admin.html',{'user_details': user_details})
    elif x == 'live session':
        today = date.today()
        pk_table = session_data.objects.filter(schedule_date=today)
        if pk_table:
            try:
                st_update = st_data.objects.get(st_date=today)
                st_update.st_status = 'start'
                st_update.save()
            except:
                new_session = st_data(st_date=today,st_status='start')
                new_session.save()
            function2 = 'schedule_data'
        else:
            messages.info(request,'आज प्रश्नोत्तरे नाही आहे ')
            return render(request,'home_sampark_sevekari.html',{'user_details': user_details})

    elif x == 'view session':
        today = date.today()
        pk_table = session_data.objects.filter(schedule_date=today)
        if pk_table:
            st_update = st_data.objects.get(st_date=today)
            if st_update.st_status == 'start':
                function2 = 'schedule_data'
            elif st_update.st_status == 'break':
                 reason = st_update.st_comment
                 msg = "प्रश्नोत्तरे थांबवली आहे,थोड्या वेळाने पुन्हा चालू होईल"+ " "+ "\n" + reason
                 messages.info(request,msg)
                 function2 = 'schedule_data'
            else:
                messages.info(request,'आजची प्रश्नोत्तरे संपले आहेत ')
                return render(request,'home_sampark_sevekari.html',{'user_details': user_details})
        else:
            messages.info(request,'आज प्रश्नोत्तरे नाही आहे ')
            return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})

    elif x == 'pk session':
        today = date.today()
        pk_table = session_data.objects.filter(schedule_date=today).filter(User_id_id=id)
        if pk_table:
            pk_table = session_data.objects.filter(schedule_date=today)
            st_update = st_data.objects.get(st_date=today)
            if st_update.st_status == 'start':
                function2 = 'schedule_data'
            elif st_update.st_status == 'break':
                reason = st_update.st_comment
                msg = "प्रश्नोत्तरे थांबवली आहे,थोड्या वेळाने पुन्हा चालू होईल" + " " + "\n" + reason
                messages.info(request, msg)
                function2 = 'schedule_data'
            else:
                messages.info(request, 'आजची प्रश्नोत्तरे संपले आहेत ')
                return render(request, 'home_prashankarta.html', {'user_details': user_details})
        else:
            messages.info(request, 'तुमचा प्रश्न आजच्या लिस्ट मध्ये नाही  ')
            return render(request, 'home_prashankarta.html', {'user_details': user_details})

    else:
        pk_table = session_data.objects.exclude(status='completed').exclude(status='rejected').exclude(status = 'submitted')
        function2 = 'schedule_data'

    userlist = createlist(pk_table)

    if pk_table:
         if user_details.type == 'sampark_sevekari':
            return render(request, 'home_sampark_sevekari.html', {'user_details': user_details,'userlist': userlist ,'function2':function2})
         elif user_details.type == 'main_admin':
            return render(request, 'home_admin.html',
                           {'user_details': user_details, 'userlist': userlist, 'function2': function2})
         elif user_details.type == 'verified':
            return render(request, 'home_prashankarta.html',
                           {'user_details': user_details, 'userlist': userlist, 'function2': function2})

    else:
        messages.info(request,'प्रश्नकर्ता नाही आहे ')
        if user_details.type == 'sampark_sevekari':
            return render(request,'home_sampark_sevekari.html', {'user_details': user_details})
        elif user_details.type == 'main_admin':
            return render(request, 'home_admin.html', {'user_details': user_details})


def upcoming_sessions(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    upcoming_dates = st_data.objects.filter(st_status='schedule').values('st_date')
    pk_table = []
    for i in upcoming_dates:
        date = i['st_date']
        pk_table1 = session_data.objects.filter(schedule_date=date)
        pk_table.append(pk_table1)
    userlist = createlist1(pk_table)
    if pk_table:
        function2 = 'upcoming sessions'
        if user_details.type == 'sampark_sevekari':
            return render(request, 'home_sampark_sevekari.html',
                          {'user_details': user_details, 'userlist': userlist, 'function2': function2})
    else:
        messages.info(request,'सध्या प्रश्नोत्तरे सेशन्स नाहीत')


def prashan_schedule(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    schedule_date = request.POST['schedule_date']
    select_timeslot = request.POST['select_timeslot']
    session_id = request.POST['select_questions']
    record = session_data.objects.get(pk=session_id)
    pkdata = get_user_model().objects.get(id=record.User_id_id)
    userlist = []
    function2 = 'ud1'
    if pkdata.type == 'unverified':
        messages.info(request,' ❗ सिलेक्ट केलेला प्रश्नकर्ता वेरिफाइड नाही आहे ❗ ')
    else:
        record.status = 'scheduled'
        record.schedule_time = select_timeslot
        record.schedule_date = schedule_date
        record.save()
        st_record = st_data.objects.filter(st_date=schedule_date)
        if not st_record:
            new_record = st_data(st_date=schedule_date,st_status='schedule')
            new_record.save()

        messages.info(request,'👍 सेशन आइडी'+'  ' + session_id + ' शेड्युल  यशस्वी 👍')
    pk_table = session_data.objects.filter(status='submitted')
    userlist = createlist(pk_table)

    return render(request, 'home_admin.html', {'user_details': user_details,'userlist': userlist ,'function2':function2})


def createlist(pk_table):
    pk_table = pk_table
    userlist = []
    for i in pk_table:
            id=i.User_id
            session_id=i.session_id
            prashan1=i.prashan1
            prashan2 = i.prashan2
            Date_filled = i.Date_filled
            status = i.status
            timeslot = i.schedule_time
            schedule_date = i.schedule_date
            userdata = get_user_model().objects.get(mobile1=id)
            full_name = (userdata.first_name)+ ' ' + (userdata.last_name)
            mobile1=userdata.mobile1
            mobile2=userdata.mobile2
            user_id=userdata.id
            city=userdata.city
            ss_code = userdata.sscode
            ss_record = sampark_sevekari.objects.filter(sscode=ss_code).values('User_id_id')
            print("ss_record:",ss_record)
            print('i have reached here')
            ss_user_id = ss_record[0]['User_id_id']
            print('value of ss_user_id : ',ss_user_id,type(ss_user_id))
            ss_data = get_user_model().objects.filter(pk=ss_user_id).values('first_name','last_name')
            print('ss_data:',ss_data)
            ss_name = ss_data[0]['first_name'] + ' ' + ss_data[0]['last_name']
            print("ss name :", ss_name)


            dic1={'user_id':user_id,'session_id':session_id,'prashan1':prashan1,'prashan2':prashan2,
                   'Date_filled':Date_filled,'city':city,'full_name':full_name,'mobile1':mobile1,
                  'mobile2':mobile2,'status':status,'timeslot':timeslot,'schedule_date':schedule_date,'ss_name':ss_name}

            userlist.append(dic1)
    return userlist



def createlist1(pk_table):
    pk_table = pk_table
    userlist = []
    for j in pk_table:
        for i in j:
            id=i.User_id
            session_id=i.session_id
            prashan1=i.prashan1
            prashan2 = i.prashan2
            Date_filled = i.Date_filled
            status = i.status
            timeslot = i.schedule_time
            schedule_date = i.schedule_date
            userdata = get_user_model().objects.get(mobile1=id)
            full_name = (userdata.first_name)+ ' ' + (userdata.last_name)
            mobile1=userdata.mobile1
            mobile2=userdata.mobile2
            user_id=userdata.id
            city=userdata.city
            ss_code = userdata.sscode
            ss_record = sampark_sevekari.objects.filter(sscode=ss_code).values('User_id_id')
            print("ss_record:",ss_record)
            print('i have reached here')
            ss_user_id = ss_record[0]['User_id_id']
            print('value of ss_user_id : ',ss_user_id,type(ss_user_id))
            ss_data = get_user_model().objects.filter(pk=ss_user_id).values('first_name','last_name')
            print('ss_data:',ss_data)
            ss_name = ss_data[0]['first_name'] + ' ' + ss_data[0]['last_name']
            print("ss name :", ss_name)


            dic1={'user_id':user_id,'session_id':session_id,'prashan1':prashan1,'prashan2':prashan2,
                   'Date_filled':Date_filled,'city':city,'full_name':full_name,'mobile1':mobile1,
                  'mobile2':mobile2,'status':status,'timeslot':timeslot,'schedule_date':schedule_date,'ss_name':ss_name}

            userlist.append(dic1)
    return userlist

def stop_session_page(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    function2 = 'stop_session'
    return render(request,'home_admin.html',{'user_details':user_details,'function2':function2})

def pause_session_page(request):
    #pause_reason = request.POST['']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    function2 = 'pause_session'
    return render(request,'home_admin.html',{'user_details':user_details,'function2':function2})


def stop_session(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    stop_date = request.POST['stop_date']
    try:
        st_update = st_data.objects.get(st_date=stop_date)
        st_update.st_status = 'stop'
        st_update.save()
    except:
        messages.info(request,'निवडलेल्या तारखेला सेशन नाही')
        return render(request, 'home_admin.html', {'user_details': user_details})

    pk_table = session_data.objects.filter(schedule_date=stop_date)
    for i in pk_table.iterator():
        if i.status == 'scheduled':
            i.status = 'pending'
            i.save()
    messages.info(request,'आजची प्रश्नोत्तरे संपले आहेत')
    return render(request, 'home_admin.html',{'user_details':user_details})

def pause_session(request):
    pause_reason = request.POST['pause_reason']
    today = date.today()
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    try:
        st_update = st_data.objects.get(st_date=today)
        st_update.st_status = 'break'
        st_update.st_comment = pause_reason
        st_update.save()
        messages.info(request, 'सेशन पॉज करण्यात आले आहे ')
        return render(request, 'home_admin.html', {'user_details': user_details})
    except:
        messages.info(request,'निवडलेल्या तारखेला सेशन नाही')
        return render(request, 'home_admin.html', {'user_details': user_details})



def pk_status(request):
    session_id = request.POST['session_id']
    pk_status = request.POST['pk_status']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    userdata = session_data.objects.get(pk=session_id)
    userdata.status = pk_status
    userdata.save()
    messages.info(request,' प्रश्नकर्ता  स्टेटस अपडेटेड')
    today = date.today()
    print("today date is:", today)
    pk_table = session_data.objects.filter(schedule_date=today)
    function2 = 'schedule_data'
    userlist = createlist(pk_table)

    if pk_table:
        return render(request, 'home_admin.html',
                      {'user_details': user_details, 'userlist': userlist, 'function2': function2})
    else:
        messages.info(request,'प्रश्नकर्ता नाही आहे ')
        return render(request,'home_admin.html', {'user_details': user_details})


def load_sevaform(request):
    session_id = request.POST['select_name']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    userdata=session_data.objects.get(pk=session_id)
    prashan1 = userdata.prashan1
    prashan2 = userdata.prashan2
    pid = userdata.User_id_id
    userdata.status = 'in progress'
    userdata.save()
    udata = get_user_model().objects.get(pk=pid)
    full_name = udata.first_name + ' ' + udata.last_name
    email = udata.email
    previous_seva = seva_data.objects.filter(session_id=session_id)
    print('previous_seva:', previous_seva)
    dic1 = {'full_name':full_name,'prashan1':prashan1,'prashan2':prashan2,'session_id':session_id,'pid':pid,'email':email}
    return render(request,'sevaform.html',{'user_details':user_details,'previous_seva': previous_seva,'dic1':dic1})


def save_seva(request):
      id = request.POST['user']
      user_details = get_user_model().objects.get(pk=id)
      if request.method == 'POST':
            sthapna = request.POST.getlist('sthapna')
            maansanam = request.POST.getlist('maansanam')
            mantrajaap = request.POST.getlist('mantrajaap')
            parayaan = request.POST.getlist('parayaan')
            yantrastapana = request.POST.getlist('yantrastapana')
            strotatvachan = request.POST.getlist('strotatvachan')
            vastudosh = request.POST.getlist('vastudosh')
            pitraseva = request.POST.getlist('pitraseva')
            otherseva = request.POST.getlist('otherseva')
            vishesh_suchana_seva = request.POST.getlist('vishesh_suchana_seva')
            session_id = request.POST['session_id']
            pid = request.POST['pid']
            email = request.POST['email']
            guru_ans_p1= request.POST['guru_ans_p1']
            guru_ans_p2 = request.POST['guru_ans_p2']

            if guru_ans_p1:
                    list = [sthapna, maansanam, mantrajaap, parayaan,yantrastapana,strotatvachan,vastudosh,pitraseva,otherseva,
                            vishesh_suchana_seva,]
                    sevalist=[]
                    pending_seva=[]
                    seva16 = ' '
                    how_to_do = ''
                    clubseva = ''
                    for i in list:
                        for j in i:
                            if len(sevalist)<=14:
                                values = select_howtodo_seva(j)
                                how_to_do = how_to_do + values['seva_descrption']
                                j= values['seva_fullform']
                                if j:
                                    clubseva = clubseva + '\n' + j
                                sevalist.append(j)

                            else:
                                values = select_howtodo_seva(j)
                                how_to_do = how_to_do + values['seva_descrption']
                                j = values['seva_fullform']
                                if j:
                                    clubseva = clubseva + '\n' +j
                                pending_seva.append(j)

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

                    nitya_seva = """ रोजची नित्य उपासना
                                     मंत्र जप:
                                        1. || श्री गुरु स्वामी समर्थ जय जय स्वामी समर्थ || * ११ वेळा *
                                        2.|| श्री स्वामी समर्थ || * 3 माळ *
                                        3. ||  शिव चिदंबर || * १ माळ *
                                     पोथी वाचन:
                                        1. स्वामी चरित्र सारामृत ( रोज १ किंवा ३ अध्याय )
                                               पोथी वाचन  क्रम : ( दिवस १ : अध्याय १ , दिवस २ : अध्याय २,.....)   किंवा 
                                               ( दिवस १: अध्याय १,२,३ ,   दिवस २ : अध्याय ४,५,६,   ....)
                                        2. दुर्गासप्तशती ( रोज २ अध्याय वाचन )
                                               पोथी वाचन  क्रम : ( दिवस १: अध्याय १,२  ,  दिवस २ : अध्याय ,३,४   ,  ....)
                                               नैवैद्य: रोज सकाळ संध्याकाळ महाराजांना नैवैद्य दाखविणे       
                                 """

                    sk1 = """  नैवेद्य :-
                                    महाराजांना सकाळी व संध्याकाळी दोन वेळा नैवेद्य दाखवायचाआहे, सकाळी जो स्वयंपाक केला
                                    असेल त्याचा नेवेद्य प्रथम महाराजांना दाखवायचा आणि त्यानंतर दहा मि नि टांनी उचलून तो प्रसाद म्हणून
                                    खायचा.
                                    संध्याकाळी सुद्धा याच पद्धतीने ताज्या केलेल्या स्वयंपाकाचा नैवेद्य दाखवायचा, 
                                    जर संध्याकाळी ताजा स्वयंपाक केला नसेल तर मग इतर कोणत्याही पदार्थां चा नैवेद्य दाखवू शकता, 
                                    जसे एक कप दूध, दूध साखर पोहे कि ंवा एखादे फळ, गुळ शेंगदाणे, ड्रायफूट कि ंवा इतर काही पण चालेल 
                                    दहा मि नि टानंतर उचलून घरातील सर्वां नी प्रसाद म्हणून खावा 
                                    अशा पद्धतीने न चुकता दोनदा सकाळी व संध्याकाळी नैवेद्य दाखवावा.
                           """

                    sk2 = """  सकाळी आंघोळीनंतर महाराजांना नमस्कार करून 11 वेळा 
                               ||श्री गुरू स्वामी समर्थ जय जय स्वामी समर्थ|| 
                               हा मंत्र म्हणावा.
                          """

                    sk3 = """  त्यानंतर तीन माळी 
                              ||श्री स्वामी समर्थ|| यामंत्राचा जप करावा, 
                              एक माळ ||शि व चि दंबर|| 
                              या मंत्राचा जप करावा.
                          """

                    sk4 = """  त्यानंतर श्री स्वामी चरित्र सारामृत पोथीचा रोज एक कि ंवा तीन अध्याय वाचावेत. घरातील स्त्रि यांनी
                                    श्रीदुर्गा सप्तशती पोथीचे रोज दोन अध्याय वाचावेत. स्वामी चरि त्र सारामृत पोथी मध्ये एकूण 21 अध्याय आहेत
                                    रोज एक कि ंवा तीन अध्याय यापद्धतीने 21 अध्याय वाचून पूर्ण झाल्यावर परत त्याच पद्धतीने पोथीचे वाचन
                                    नेहमी चालू ठेवायचे आहे. तसेच श्री दुर्गा सप्तशती पोथीमध्ये13 अध्याय आहेत .पहि ल्या दि वशी पोथी मधील
                                    सुरुवातीची संपूर्ण माहि ती वाचून पहि ला व दुसरा असेदोन अध्याय वाचावेत. मात्र दुसऱ्या दि वशी सरळ अध्याय
                                    क्रमांक 3 पासून सुरुवात करावी. या पद्धतीने रोज दोन अध्याय श्री दुर्गा सप्तशती पोथीचे वाचावे. शेवटच्या दि वशी
                                    अध्याय तेरावा वाचन करून त्यापुढील सर्व माहि ती वाचावी अशा प्रकारे रोज वाचन चालू ठेवायचे आहे...
                                    👉सूचना:-घरांमधील स्त्री वाचू शकत नसेल तर श्री दुर्गा सप्तशतीचेअध्याय पुरुषांनी वाचायला हरकत नाही. 
                                    या दुर्गा सप्तशती पोथीमध्येच दुर्गा त्रि शतीपोथी दि ली आहेती रोज वाचायची नाही आहे.*
                                    """

                    sk5 = """ 5.पंचमहायज्ञामध्ये पुढील पाच गोष्टी कराव्यात 1)अग्नीला तूप- कागदाचा तुकडा जाळून त्यावर एक थेंब तूप
                                    टाकावे. 2) गायीला नैवेद्य:- केलेल्या स्वयंपाकातून रोज एक नैवेद्य काढून गाईला लावावा 3)मग्ंु यांना साखर:-
                                    घरातील कळ्या मग्ंु यांना दोन चार दाणे साखर रोज टाकावी 4)कावळ्याला घास:- दपु ारी 12 नतं र घराच्या दक्षि ण
                                    दि शेला एक घास कावळ्यासाठी ठेवावा,5)अथि तीला चहापाणी:- घरी कोणीही आल्यास त्यांना चहा-पाणी करावा
                                    अशा पद्धतीने पंचमहायज्ञ न चुकता रोज करावा....
                                    टीप :-सुतकाच्या काळात (घरी मृत्यू झाल्यास)13 दि वस, वृद्धीच्या काळात(नवीन बाळाचा जन्म झाल्यास) 10
                                    दि वस व स्त्रि यांच्या अडचणीच्या काळात 4 दि वस सेवा बंद ठेवाव्यात.
                                    सेवा क्रमांक"""
                    nitya_seva_details = sk1 + '\n' + sk2 + '\n' + sk3 + '\n' + sk4 + '\n' + sk5
                    y1   = """
                               🌸  🌸  दिलेली सेवा कशी करावी ती खालीलप्रमाणे आहे 🌸  🌸 
                               
                           """
                    msg = nitya_seva + '\n' + clubseva + '\n' + y1 + '\n' + nitya_seva_details + '\n' + how_to_do
                    send_mail('दिलेली सेवा ', msg, 'samarthview@gmail.com',
                              [email, 'gurumargdarshan14@gmail.com'], fail_silently=True)

                    function2 = 'ds'
                    return render( request,'home_admin.html',{'user_details': user_details, 'display_seva': sevalist, 'pending_list':pending_seva, 'function2': function2})
            else:
                return render(request, 'home_admin.html', {'user_details': user_details})
      else:
          return render(request, 'home_admin.html', {'user_details': user_details})


def load_showseva():

    return redirect('show_selectedseva.html')



def select_howtodo_seva(seva):
    seva = seva
    seva_details = ''
    dic1 = {
        'sk1': ' सेवा १ : नैवद्य -सकाळी व सायंकाळी स्वामींना ताज्या अन्नाचा नैवद्य दाखवावा.सायंकाळी ताज्या अन्नाचा नैवद्य शक्य नसेल तर फळ /दुधाचा  नैवद्य दाखवावा',
        'sk2': ' सेवा २ : दररोज अकरा वेळा ।।  || श्री गुरु स्वामी समर्थ जय जय स्वामी समर्थ || हा मंत्र म्हणावा ',
        'sk3': '  सेवा ३ : दररोज तीन माळी  ।। श्री स्वामी समर्थ ।। मंत्रजप व एक माळ ।। शिव चिदंबर ।। मंत्रजप करावा',
        'sk4': ' सेवा ४ : स्वामी चरित्र सारामृत ( रोज १ किंवा ३ अध्याय वाचावे ),दुर्गासप्तशती ( रोज २ अध्याय वाचावे  )',
        'sk5': 'सेवा ५ : रोज पंचमहायज्ञ करावा (अग्नीला तूप, गाईला नैवद्य, मुंगीला साखर , कावळ्याला घास दुपारी १२ नंतर , अतिथीला चहा पाणी करणे )',
        'sk6': ' सेवा ६ : श्री स्वामी समर्थ महाराजांच्या फोटोची स्थापना देवघरात मध्यभागी करावी',
        'sk7': ' सेवा ७ : महादेवाच्या पितळेची पिंड (नंदी नाग जोडून नसलेली )स्थापना / पुनर्स्थापना करावी.',
        'sk8': ' सेवा ८ : गणपतीची पितळेची मुर्ती स्थापना / पुनर्स्थापना करावी',
        'sk9': ' सेवा ९ : बालकृष्णाची  पितळेची मुर्ती स्थापना / पुनर्स्थापना करावी',
        'sk10': ' सेवा १० : अन्नपूर्णा देवीची पितळेची  मुर्ती स्थापना / पुनर्स्थापना करावी.',
        'sk11': '  सेवा ११ : कुलदेवी /कुलदेवता मानसन्मान करून  विनंती करावी.',
        'sk12': ' सेवा १२ : ग्रामदेवता मानसन्मान करून  विनंती करावी.',
        'sk13': ' सेवा १३ : शेतातील सेंद्रिय देवतांचा मानसन्मान करून विनंती करावी (शनिवार किंवा अमावस्या )',
        'sk14': ' सेवा १४ : आरतीला जाण्याची सेवा',
        'sk15': ' सेवा १५ : सोमवारी महादेवाच्या मंदिरात जलाभिषेक ब्राह्मणाकडून करावा व विनंती करून तीर्थप्रसाद घ्यावा',
        'sk16': ' सेवा १६ : शिव चिदंबर १०८ माळी (एकदाच करावा)',
        'sk16_1': ' सेवा १६_१ : श िव चिदंबर  सव्वा लक्ष (एकदाच करावा) ',
        'sk17': 'सेवा १७ : श्री स्वामी समर्थ - १०८ माळी (एकदाच करावा)',
        'sk17_1': ' सेवा १७_१ :श्री स्वामी समर्थ - सव्वा लक्ष (एकदाच करावा)',
        'sk18': ' सेवा १८: गायत्री मंत्र जप. २४ वेळा - १ दिवस',
        'sk19': ' सेवा १९ : ॐ ह्रीं नमः जप ११वेळा - ११ दिवस',
        'sk20': 'सेवा २० : मधुमती मंत्र जप ११वेळा - ११ दिवस ',
        'sk21': ' सेवा २१ : श्री स्वामी सारामृत पोथी पारायण ( एक वेळा  करावे ) ',
        'sk21_1': ' सेवा २१_१ : श्री स्वामी सारामृत पोथी पारायण ( तीन वेळा करावे )',
        'sk22': ' सेवा २२ : श्री दुर्गासप्तशती पारायण ( एक वेळा  करावे )',
        'sk22_1': 'सेवा २२_१: श्री दुर्गासप्तशती पारायण ( तीन वेळा करावे )',
        'sk23': 'सेवा २३ : श्री दुर्गा त्रिशती पारायण ( एक वेळा  करावे )',
        'sk23_1': ' सेवा २३_१ : श्री दुर्गा त्रिशती पारायण ( तीन वेळा  करावे )',
        'sk24': 'सेवा २४ :श्री गुरु चरीत्र (प.पु. टेंबे स्वामींचे )',
        'sk25': ' सेवा २५ :श्री शिवलीलामृत पोथी पारायण (३ किंवा ५ दिवसाचे )',
        'sk26': ' सेवा २६ : श्री दत्त महात्म्य पारायण ',
        'sk27_2': ' सेवा २७_२ : श्री नवनाथ पारायण',
        'sk27': ' सेवा २७ : श्री नवनाथ १५ वा अध्याय वाचणे - ३‌ दिवस (रोज एक वेळ) ',
        'sk27_1': ' सेवा २७_१ : श्री नवनाथ ५ वा अध्याय वाचने. ३‌ दिवस (रोज एक वेळ)',
        'sk28': ' सेवा २८ : एका पौर्णिमेला सत्यनारायण पूजा करून पोथी वाचावी ',
        'sk29': 'सेवा २९ : श्रीयंत्र स्थापणा (पोर्णिमेला)',
        'sk30': ' सेवा ३० : मारुती यंत्र ',
        'sk31': 'सेवा ३१ : ६४ योगीनी यंत्र (प्रवेश द्वारावर दु्र्गा अष्टमीला लावणे)',
        'sk32': ' सेवा ३२ : सुर्य यंत्र ',
        'sk33': ' सेवा ३३ : वाहन यंत्र ',
        'sk34': ' सेवा ३४ : वास्तु यंत्र ',
        'sk35': ' सेवा ३५ : पंचमुखी हनुमान स्तोत्र वाचन',
        'sk36': ' सेवा ३६ : हनुमान वडवानल स्तोत्र वाचन ',
        'sk37': ' सेवा ३७ : लांगुलास्त्र स्तोत्र वाचन(मारोतीच्या मंदिरात किंवा फोटोसमोर शनिवारी).',
        'sk38': ' सेवा ३८ : कालभैरवाष्टक स्तोत्र वाचन',
        'sk39': ' सेवा ३९ :महालक्षम्याष्टकम स्तोत्रवाचन ',
        'sk40': ' सेवा ४० : व्यंकटेश स्तोत्र वाचन ',
        'sk41': ' सेवा ४१ :श्रीसुक्त वाचन',
        'sk42': 'सेवा ४२ : दर रविवारी सुर्याला जल देणे',
        'sk43': ' सेवा ४३ : महामृत्युंजय कवच वाचुन तिर्थ घेणे',
        'sk44': 'सेवा ४४ : वलगा सुक्त नाडीवर वाचने',
        'sk45': ' सेवा ४५ : ललीता सहस्त्रनाम स्तोत्र वाचन',
        'sk46': ' सेवा ४६ : रात्री सुक्त वाचन ',
        'sk47': ' सेवा ४७ : चक्षु स्तोत्र एकदा वाचणे',
        'sk48': ' सेवा ४८ : विष्णु सहस्त्रनाम वाचन ',
        'sk49': ' सेवा ४९ : गायत्री सहस्त्रनाम एकदा वाचणे ',
        'sk50': ' सेवा ५० : गणपती अथर्वशिर्ष वाचन ',
        'sk51': ' सेवा ५१ : रामरक्षा स्तोत्र १ वेळा वाचने.',
        'sk52': ' सेवा ५२ : रुख्मिणी स्वयंवर वाचणे',
        'sk53': ' सेवा ५३ : वास्तुदोष निवारण सेवा',
        'sk54': ' सेवा ५४ : त्र्यबंकेश्वरला  नारायण नागबळी  करावी  ',
        'sk55': ' सेवा ५५ : मातृदोष निवारण सेवा',
        'sk56': ' सेवा ५६ : आठवड्यातून एखाद्या दिवशी गाईच्या तुपाचा किंवा तिळाच्या तेलाचा दिवा देवघरात लावावा',
        'sk57': ' सेवा ५७ : रोज सकाळी एक चमचा गोमुत्र अर्क घेणे',
        'sk58': ' सेवा ५८ : कडुलिंबाच्या पानाचा एक चमचा रस एक कप पाण्यात टाकून तीन दिवस घ्यावा',
        'sk59': ' सेवा ५९ : कुलदेवीची टाक/ मुर्तीवरील हळद दुधातुन घेणे ',
        'sk60': ' सेवा ६० : एक चमचा मध घेऊन त्यावर प्रत्येकी अकरा वेळा ।। श्री स्वामी समर्थ ।। व ।। शिव चिदंबर ।।  मंत्र जप म्हणून ते खाऊन घ्यावेत ',
        'sk61': ' सेवा ६१ : कुंकुमार्चन विधीचे कुंकू आपल्या पतीचे ध्यान करून रोज कपाळाला लावावेत',
        'sk62': ' सेवा ६२ : पक्षांना तांदुळ टाकणे/ पाणी टाकणे ',
        'sk63': ' सेवा ६३ : देवघरात जप युनीट लावणे ',
        'sk64': ' सेवा ६४ : देवघर देव्हारा मठाकडुन तपासुन घेणे ',
        'sk65': ' सेवा ६५ : कोणत्याही गोशाळेत  वर्षातून एकदा पैसे देण्याऐवजी यथाशक्ती चारा दयावा.',
        'sk66': ' सेवा ६६ : अन्नदान  यथाशक्ती करावे : वर्षातून एकदा कमीत कमी पाच लहान मुलांना जेऊ घालावे.',
        'sk67': ' सेवा ६७ : दही भात उतारा (शुक्रवारी दुपारी १२ नंतर).',
        'sk68': ' सेवा ६८ : मोरपीस उतारा (शनिवार / अमावस्या) ',
        'sk69': ' सेवा ६९ : नारळ  उतारा (शनिवार/अमावस्या)',
        'sk70': ' सेवा ७० : आसरांची सेवा (शुक्रवारी) फक्त महिलांनी ',
        'sk71': ' सेवा ७१ :  पांढर्या मोहरीची‌ सेवा (शनिवार/अमावस्या) ',
        'sk72': ' सेवा ७२ : मारोतीच्या मंदिरात दिव्यात तेल टाकणे (१ शनिवारी) ',
        'sk72_1': 'सेवा ७२_१ : मारोतीच्या मंदिरात दिव्यात तेल टाकणे (३ शनिवारी) ',
        'sk73': ' सेवा ७३ : एका शनिवारी शनिमंदिरात  पुरुषांच्या हातून टाकावेत ',
    }

    sk6 = """ 
              सेवा ६ : श्री स्वामी समर्थ महाराजांचा फोटो देवघरात मध्यभागी ठेवावा 
              महाराजांचे अष्टगंध लावून रोज पूजन करावे.
          """
    sk7 = """  
               सेवा ७ : महादेवाच्या पि डं ीची (नदं ी नाग जोडून नसलेली) 
               स्थापना कि ं व पनु र्स्था पना जे काही सांगि तले असेल ते
               ब्राह्मणांच्या हस्ते देवघरात करावे
          """
    sk8 = """ 
               सेवा ८ : गणपतीची पितळेच्या मूर्ती ची स्थापना कि ंवा पुनर्स्था पना जे सांगि तले असेल ते ब्राह्मणांच्या हस्ते देवघरात
                       करावे. 
          """
    sk9 = """
               सेवा ९ : बाळकृष्णाच्या पि तळेच्या मूर्ती ची स्थापना कि ंवा पुनर्स्था पना जे सांगि तले असेल ते ब्राह्मणांच्या हस्ते देवघरात
          """
    sk10 = """ 
              सेवा १० : अन्नपूर्णा देवीच्या पि तळेच्या मूर्ती ची स्थापना कि ंवा पुनर्स्था पना जे सांगि तले असेल ते ब्राह्मणांच्या हस्ते
                        देवघरात करावे.
           """
    sk11 = """ 
              सेवा ११ : कुलदेवी कुलदेवतांचा मान सन्मान
                          शक्य तेवढ्या लवकर कुलदेवीच्या मूळ ठि काणी जाऊन देवीचा मान सन्मान करावा.
                          देवीची ओटी भरावी शक्य असल्यास साडीचोळी करावी व देवीला नारळ ठेवून वि नंती करावी.
                          आपल्या अडचणी देवीला सांगाव्यात.त्याचप्रमाणे आपल्या कुलदेवतेला जाऊन मानसन्मान करावा
                          कारंज्याच्या गुरु महाराजांनी पाठवि ले असे सांगावे,वि नंती करावी.
           """

    sk12 = """ 
              सेवा १२ : ग्रामदेवतांचा मान सन्मान
                         आपण ज्या गावात राहतो त्या गावातील देवतांना ग्रामदेवता म्हणतात गावातील तीन कि ंवा पाच वेगवेगळ्या
                         देवतांच्या मंदि रात जाऊन त्या देवांची पूजा करावी. 
                         प्रत्येक मंदि रात जाऊन नारळ हातात पकडून देवांना पुढील प्रमाणे विनंती करावी. 
                         नारळाची शेंडी देवाकडे असली पाहिजे . अशा पद्धतीने नारळ हातामध्ये पकडा त्यानंतर गुरु आदेशानुसार विनंती करतो 
                         असे बोलून आपल्या अडचणी देवांना सांगाव्यात व त्या अडचणींमधून मार्ग मिळावा अशी विनंती करावी.व
                  
                          ि नंती पूर्ण झाल्यानंतर नारळ देवासमोर ठेवून द्यावे (नारळ फोडू नये). 
                         अशा प्रकारे तीन कि ंवा पाच वेगवेगळ्या देवतांच्या मंदि रात जाऊन प्रत्येक देवाला नारळ हातामध्ये पकडून विनंती 
                         प्रार्थना करावी.ही सेवा एकदाच करायची आहे त्यामुळे रोज पाच मंदि रात जायचेनाही.
           """
    sk13 = """ 
              सेवा १३ :  शेतातील सेंद्रि य देवतांचा मानसन्मान
                          शेतातील शेंदूर लावलेल्या देवता म्हणजे सेंद्रि य देवता होय. शनि वारी कि ंवा अमावस्येला या देवांना शेंदूर लावावा
                          दि वाबत्ती करावी व नारळ फोडून त्याच ठि काणी टाकून द्यावे. नमस्कार करावा आणि शेती उत्पन्न करि ता वि नंती
                          करावी. शेतामध्ये जर म्हसोबा देवता असेल तर म्हसोबांकरि ता बाजरीची भाकरी, वांग्याचं भरीत व पातीचा कांदा
                          यांचा नैवेद्य ठेवावा,नारळ फोडून त्याच ठि काणी सोडून द्यावे. ज्यांच्या शेतामध्ये सेंद्रि य देवता नाहीत त्यांनी
                          शेजारील शेतांमध्ये असलेल्या देवतांची पूजा करावी.
           """
    sk14 = """ 
              सेवा १४ : आरतीला जाण्याची सेवा
                        दत्त मंदि र चोहट्टा बाजार कि ंवा गुरु मंदि र कारंजा लाड कि ंवा दत्त मंदि र हि गं णघाट 
                        कि ं वा श्री नसिृहं सरस्वती  स्वामी महाराज मठ पाटी. यापैकी ज्या ठि काणी नारळ ठेवून विनंती करायला
                        सांगि तले असेल त्या ठि काणी जाऊन नारळ ठेवून वि नंती करावी व सांगि तल्यानुसार एक कि ंवा तीन आरत्यांना हजर राहावे 
                         व तीर्थप्रसाद घ्यावा.जाण्यापूर्वी त्या ठि काणावरील सेवेकऱ्यांशी फोनवरून संपर्क करून आरतीची वेळ माहिती करून घ्यावी.
           """

    sk15 = """ 
              सेवा १५ : महादेवाचा जलाभि षेक
                          सोमवारी मदिं रात जाऊन महादेवाच्या पि डं ीवर जलाभि षके ( पाण्याचा अभि षके ) करावा.आपल्या अडचणी भगवान
                          शंकराला सांगाव्यात व वि नंती करावी. अभिषेकाची पूजा ब्राम्हणाकडून कडूनच करायची आहे,त्यामुळे तुमच्या
                          ओळखीच्या पजु ारी ब्राह्मणाला भेटून अधि क माहि ती घ्यावी.
                          अभिषके ाचे पि डं ीवरील थोडसे े तीर्थ एका डबीमध्ये आणावे व सर्वां नी ते घ्यावे. 
                          आजारी व्यक्तींकरि ता जलाभि षेक सांगि तला असल्यास तो कोणत्याही दि वशी करता येईल.
                          तसेच अभि षेकाचे तीर्थ आजारी व्यक्तींना द्यावेत्यांच्यासाठी ते फार महत्त्वाचे आहे
                          
           """

    sk16 = """ 
                सेवा १६ : ||शि व चि दंबर|| मंत्र जप 108 माळी
                        शि व चि दंबर हे पृथ्वीवरील भगवान शंकराचे स्वरूप होय.
                        ||शि व चि दंबर|| मंत्रजप करण्याने भगवान शंकराचा आशीर्वा द मि ळतो. ||शि व चि दंबर|| या मंत्राचा 108 माळी जप
                        करायचा आहे. घरातील सर्वां नी मि ळून 108 माळी जप केल्यास हरकत नाही.प्रत्येकांनी कि ती माळी जप केला
                        त्याचा हि शेब ठेवावा,कोणी कि तीही माळी जप केल्यास हरकत नाही मात्र सर्वां च्या मि ळून 108 माळी होणे
                        आवश्यक आहे.अशा प्रकारे एका आठवड्याच्या आत. 
                        शि व चि दंबर मंत्राचा 108 माळी जप पूर्ण करावा.रोजच्या
                        सेवेतील एक माळ यामध्ये पकडू नये. जप जर सव्वा लक्ष सांगि तला असेल तर सांगि तल्या प्रमाणे तेवढा मोजून करावा.
                        हा जप करण्यासाठी वि शि ष्ट वेळेचे बंधन नाही,त्यामुळे कोणत्याही वेळेला आपण जप करू शकता.
            """

    sk16_1 = """  
                सेवा १६_१ : ||शि व चि दंबर|| मंत्र जप सव्वा  लक्ष
                            शि व चि दंबर हे पृथ्वीवरील भगवान शंकराचे स्वरूप होय.
                            ||शि व चि दंबर|| मंत्रजप करण्याने भगवान शंकराचा आशीर्वा द मि ळतो. 
                            ||शि व चि दंबर|| या मंत्राचा सव्वा लक्ष जप करायचा आहे. घरातील सर्वां नी मि ळून सव्वा लक्षी जप केल्यास हरकत नाही.
                            प्रत्येकांनी किती माळी जप केला त्याचा हिशेब ठेवावा,कोणी कि तीही माळी जप केल्यास हरकत नाही मात्र सर्वांच्या मिळून सव्वालक्ष जप 
                            होणे आवश्यक आहे.
                            हा जप करण्यासाठी वि शि ष्ट वेळेचे बंधन नाही,त्यामुळे कोणत्याही वेळेला आपण जप करू शकता.
              """

    sk17 = """ 
                सेवा १७  : ll श्री स्वामी समर्थ ll मंत्राचा 108 माळी
                            ll श्री स्वामी समर्थ ll या मंत्राचा 108 जप माळी करायचा आहे. घरातील सर्वां नी मि ळून 108 माळी केल्यास हरकत
                            नाही.प्रत्येकांनी कि ती माळी जप केला त्याचा हि शेब ठेवावा,कोणी कि तीही माळी जप केल्यास हरकत नाही मात्र
                            सर्वां च्या मि ळून 108 माळी होणे आवश्यक आहे.अशा प्रकारेएका आठवड्याच्या आत ||श्री स्वामी समर्थ|| मंत्र जप
                            108 माळी पूर्ण कराव्या. रोजच्या सेवेतील तीन माळी यामध्येपकडू नये. जप जर सव्वा लक्ष सांगि तला असेल तर
                            सांगितल्या प्रमाणे तेवढा मोजून करावा.
           """

    sk17_1 = """  
                सेवा १७_१:  ll श्री स्वामी समर्थ ll मंत्राचा जप सव्वा  लक्ष
                              घरातील सर्वां नी मि ळून सव्वा लक्षी जप केल्यास हरकत नाही.
                              प्रत्येकांनी कि ती माळी जप केला त्याचा हिशेब ठेवावा,कोणी कि तीही माळी जप केल्यास हरकत नाही मात्र सर्वां च्या मि ळून सव्वालक्ष जप  होणे
                              आवश्यक आहे. 
                              हा जप करण्यासाठी वि शि ष्ट वेळेचे बंधन नाही,त्यामुळे कोणत्याही वेळेला आपण जप करू शकता.
                    
             """
    sk18 = """
               सेवा १८ : गायत्री मंत्र जप 24 वेळा एक दि वस करायचा आहे. कि ंवा सांगि तलेल्या संख्येनुसारच करायचा आहे. 
    
                               आपल्या मानाने जप अधीक दि वस करू नयेत. गायत्री मंत्र नि त्योपासना पुस्तकात दि ला आहे.
           """
    sk19 = """ 
               सेवा १९ :||ओम ऱ्हीम नमः|| मंत्र जप
                       ||ओम ऱ्हीम नमः|| या मंत्राचा जप 11 वेळा, सतत 11 दि वस करायचा आहे.11 दि वस पूर्ण झाल्यावर जप बंद
                        करावा.
           """
    sk20 = """ 
               सेवा २० : मधुमती मंत्राचा जप 11 वेळा 11 दि वसच करायचा आहे. त्यांनतर जप करू नयेत.
           """

    sk21 = """
               सेवा २१ : श्री स्वामी चरित्र सारामृत पोथी पारायण (एक/तीन)
                        पाटावर लाल कापड टाकून त्यावर श्री स्वामी चरि त्र सारामृत पोथी ठेवावी व ति ची पूजा करून एक माळ ||श्री स्वामी
                        समर्थ|| मंत्र जप करावा, एक माळ || शि व चि दंबर || मंत्र जप करावा. प पू गुरुवरायांचे स्मरण करून नमस्कार
                        करावा व पोथी वाचायला सुरुवात करावी.पोथीमध्ये एकूण 21 अध्याय आहेत पूर्ण पोथी एका बैठकीत वाचणे
                        म्हणजे एक पारायण पुर्ण करणे होय. 
                        ज्यांना एका बैठकीत पुर्ण पोथी वाचणे शक्य नसल्यास एकाच दि वशी 7-7-7 अध्याय तीन टप्प्यात वाचू शकता. 
                        खाली बसून वाचता येत नसल्यास खुर्ची वर बसून सुद्धा वाचू शकता.
                        अशा प्रकारे पूर्ण पोथी एका दि वसात वाचून झाली म्हणजे एक पारायण झाले असे समजावे. 
                        पारायण गुरुवारी सकाळी करावे ज्यांना सकाळी वेळ नाही त्यांनी दुपारी पारायण केल्यास हरकत नाही कि ंवा
                        सुट्टीच्या दि वशीपण पारायण करू शकता. एकूण कि ती पारायणे सांगि तली आहेत हे बघून एका दिवशी एक अशा पद्धतीने मोजून पूर्ण करावे.
                
           """

    sk22 = """ 
                सेवा २२ : श्री दुर्गा सप्तशती पारायण (एक/तीन)
                                मंगळवारी कि ंवा शुक्रवारी एका पाटावर स्वच्छ कापड टाकून त्यावर श्रीदुर्गा सप्तशती पोथी ठेवावी. हळद-कंु कू
                                अक्षता आणि फूल वाहून एक माळ || श्री स्वामी समर्थ || व एक माळ || शि व चि दंबर || या मंत्राचा जप करावा.
                                गुरुवर्यां चे स्मरण करून पोथी वाचायला सुरुवात करावी.
                                पोथी मध्ये एकूण 13 अध्याय आहेत पान क्र.1 पासून तर 68 पर्यंत पूर्ण पोथी वाचून काढली म्हणजे एक पारायण पूर्ण होईल.
                                अशाप्रकारे एकूण कि ती पारायणे सांगितली आहे ते बघून त्यानुसार करावे. तीन पारायण सांगि तले असल्यास 
                                मंगळवार, शुक्रवार व मंगळवार या तीन दिवशी पूर्ण करावे कि ंवा सलग तीन दि वसात तीन पारायण या पद्धतीनेकेल्यास हरकत नाही. 
                                याच पोथी मध्ये दुर्गा त्रि शती पोथी दि ली आहे. श्री दुर्गा सप्तशती परायणासोबत दुर्गा त्रीशती वाचू नये.
             """

    sk23 = """  
                सेवा २३ : श्रीदुर्गा सप्तशती पोथी मधेच दुर्गा त्रि शती दि ली आहे.मंगळवारी पोथीची पूजा करून एक माळ 
                                ||श्री स्वामी समर्थ|| व एक माळ ||शि व चि दंबर|| 
                                 मंत्र जप करून दुर्गा त्रि शती पूर्ण वाचून काढावी.
                                 
           """

    sk24 = """ 
                सेवा २४ : द्वि साहस्री गुरु चरि त्र पारायण/गुरुचरि त्र कथासार 3 पारायणे
                                प.पू.टेंभे स्वामी यांचे सात दि वसीय द्वि साहस्री गुरुचरि त्र पारायण कसे करावे याबद्दल माहि ती प्रथम दि ली
                                आहे.परंतु ज्या भक्तांना सात दि वसीय पारायण करणे शक्य नाही ते भक्त संक्षि प्त गुरुचरि त्र ज्यालाच गुरुचरि त्र
                                कथासार (नि यम नसलेले)म्हणतात त्याची तीन पारायणे करावी लागतील.
                                द्वि सहासी गुरुचरि त्र पारायण पद्धती:-
                                श्री गुरुचरि त्र पोथीचे पारायण सात दि वसाचे आहे. कोणत्या दि वशी कि ती अध्याय वाचावेत याची माहि ती
                                पोथीच्या सुरुवातीला पान क्रमांक 42 वर दि लेली आहे.सात दि वस त्याच पद्धतीने अध्याय वाचावेत.महत्वाचे
                                म्हणजे टेंभे स्वामींचे द्वि सहासी गुरुचरि त्र पारायण स्त्रि या सुद्धा करू शकतात..
                                पारायण सुरु करण्याच्या एक दि वस आधी सायंकाळी सातच्या सुमारास पाटावर कि ंवा चौरंगावर स्वच्छ
                                कापड (ब्लाउज पीस) टाकून पोथी ठेवावी.बाजूला एक नारळ ठेवून पूजा करावी.त्यानंतर पाच पोळ्यांचा नैवेद्य
                                करून एक गाय व चार कुत्र्यांना खायला द्याव्यात. 
                                दुसऱ्या दिवशी सकाळी पारायणाला सुरुवात करावी. पारायण सुरू करण्याआधी एक माळ ||श्री स्वामी समर्थ|| व 
                                एक माळ ||शि व चि दंबर|| मंत्र जप करावा गुरुवर्य यांचे स्मरण करून नमस्कार करावा. व पोथी वाचायला सुरुवात करावी. 
                                सातही दि वस याच पद्धतीने करायचे आहे.सात दिवस सायंकाळी पोथीची पूजा करून वि ष्णुसहस्त्रनाम वाचायचेआहे.
                                याचे महत्त्व पारायण करताना झालेल्या चुकांतून माफी मि ळावी यासाठी आहे.. 
                                आठव्या दिवशी महाराजांना नैवेद्य दाखवावा व शक्य असल्यास एक सेवेकरी जोडपे जेवू घालावे...*
                                पारायण कालावधीमध्ये खालील नियम पाळावेत..
                                1. सात दि वस जेवणामध्ये लसूण कांदा यांचा वापर करू नये.
                                2.पारायण करणाऱ्या व्यक्तीने 7 दि वस बाहेरचे खाणे पि णेटाळावे.
                                3.सात दि वस सतरंजीवर झोपावे.
                                4.ब्रह्मचर्या चे पालन करावे
              """
    sk25 = """ 
                सेवा २५ : शिवलीलामृत पोथी पारायण
                    या पारायणला कोणतेही नि यम नाहीत.. पोथी मध्येएकूण 14 अध्याय दि लेले आहे. संपूर्ण पोथी तीन कि ंवा
                    जास्तीत जास्त पाच दि वसांमध्ये वाचून काढायची आहे. पाटावर स्वच्छ कापड टाकून पोथी ठेऊन पूजा करावी.
                    वाचायला सुरुवात करण्या आधी एक माळ ||श्री स्वामी समर्थ|| व एक माळ ||शि व चि दंबर|| हा जप करावा.
                    प.पू.गुरुवर्यां ना नमस्कार करून पोथी वाचायला सुरुवात करावी. पारायणा दरम्यान बाहेरचे खाणे पि णे टाळावे.
           """
    sk26 = """ 
               सेवा २६ : श्री दत्त महात्म्य पारायण
           """
    sk27_2 = """
               सेवा २७_२: श्री नवनाथ पारायण
             """
    sk27 = """ 
               सेवा २७ : नवनाथ पोथीचा पाचवा कि ंवा पंधरावा अध्याय वाचन सेवा.
                    दि लेल्या पोथीमध्ये पाचवा व पंधरावा असे दोनच अध्याय आहेत. 
                    तुम्हाला जो अध्याय सांगितला असेल तो अध्याय तीन दि वस रोज एकवेळा पूर्ण वाचून काढायचा आहे.
           """

    sk28 = """ 
              सेवा २८ : सत्यनारायण पोथी वाचन सेवा
                            एका पौर्णि मेला सत्यनारायण पूजेची मांडणी करून पूजन करावे. व पोथी वाचून काढावी. 
                            त्यानंतर नैवेद्य दाखवावा व आरती करावी. पूजेची मांडणी सत्यनारायण पोथीच्या मुखपृष्ठाच्या मागच्या भागावर दिली आहे.
                            त्याप्रमाणे मांडणी करून पूजन करावे.
          """

    sk29 = """ 
              सेवा २९ : श्री यंत्र स्थापना /पुनर्स्था पना
                            श्री यंत्राची स्थापना पौर्णि मेला करावी.प्रथम यंत्र पाटावर ठेवून दोन, तीन थेंब स्वच्छ पाणी टाकून पुसून काढावे.
                            यत्रं ावर हळद, कंु कू , अष्टगधं , अक्षदा फु ल वाहावे. धपू -दीप दाखवावा, डाळि ंबाच्या दाण्याचा कि ं वा खडी साखरेचा
                            नैवेद्य दाखवावा. 
                            त्यानंतर एक माळ ||श्री स्वामी समर्थ|| जप व एक माळ ||शि व चि दंबर|| मंत्रजप करावा. अकरा
                            वेळा कमलात्मक मंत्र 11 वेळा षोडशी मंत्र 11 वेळा कुबेर मंत्र म्हणावे, एक वेळा श्री सूक्त व एक वेळा
                            महालक्ष्मीअष्टक स्तोत्र वाचावे. स्वामींना, कुलदेवीला व श्री यंत्राला आर्थि क प्रगती करि ता प्रार्थना करावी.
                            श्रीयंत्र देवघरात ठेवनू हळद-कंु कू वाहून दररोज पजू ा करावी.श्रीयंत्र स्थापनेकरि ता लागणारे स्तोत्र व 
                            सर्व मंत्र नि त्योपासना पुस्तकात दि ले आहे.
                
           """

    sk30 = """ सेवा ३० : मारुती यंत्र स्थापना
                            मंगळवारी दुपारी बाराच्या सुमारास यंत्रावर दोन-चार थेंब स्वच्छ पाणी टाकून पुसून काढावे.यंत्र पाटावर ठेवून
                            अष्टगंध,अक्षता,फूल वाहावे. धूपदीप दाखवावा.खडीसाखरेचा नैवेद्द दाखवावा. त्यानंतर एक माळ ||श्री स्वामी
                            समर्थ|| व एक माळ ||शि व चि दंबर|| जप करावा. परम पूज्य गुरुवर्यां चे स्मरण करून नमस्कार करावा अशा प्रकारे
                            यंत्र सि द्ध होईल.
                            मारुती यंत्र ज्या ठि काणी ठेवायला सांगि तले असेल ति थेठेवावेत उदाहरणार्थ घरात कि ंवा प्लॉट मध्ये कि ंवा शेतात
                            ठेवायला सांगि तले असल्यास, ईशान्य कोपऱ्याला फूटभर खड्डा करून त्यात मारुती यंत्र पुरावेत.
                            घरात खड्डा करणे शक्यच नसल्यास ईशान्य कोपऱ्याला छताच्या अगदी जवळ कुणाचाही हात लागणार अशा ठि काणी एक
                            पाटी ठोकावी व यंत्राला लाल कापडात गडंु ाळून त्यावर ठेऊन द्यावे.
                            सूचना:-मारूती यंत्राची स्थापना पुरुषांच्या हातूनच करावी
                            मारुती यंत्र जवळ ठेवायला सांगि तले असल्यास जवळ ठेवावे.
            """
    sk31 = """ 
             सेवा ३१ : चौसष्ट योगिनी यंत्र स्थापना
                            दुर्गा ष्टमीच्या दि वशी यंत्रावर सकाळी दोन-चार थेंब स्वच्छ पाणी टाकून पुसून काढावे. त्यानंतर यंत्र पाटावर ठेवून
                            हळद, कंु कू , अष्टगधं , अक्षदा, फु ल ं वाहावे. धपू दीप दाखवावा. त्यानतं र खडी साखरेचा नवै ेद्य दाखवनू एक माळ
                            ||श्री स्वामी समर्थ|| व एक माळ ||शि व चि दंबर|| जप करावा.
                            परम पूज्य गुरुवर्यां चे स्मरण करून नमस्कार करावा.अशा प्रकारे यंत्र सि द्ध होईल.
                            हे यंत्र मुख्य द्वाराच्या बाहेरून मध्यभागी चि टकावे. दर दुर्गा ष्टमी ला यंत्राची पूजा करावी.
           """
    sk32 = """ 
              सेवा ३२ : सूर्य यंत्र स्थापना
                            रवि वारी सकाळी यंत्र पाटावर ठेवून दोन-चार थेंब स्वच्छपाणी टाकून पुसून काढावे.यंत्र पाटावर ठेवून अष्टगंध,
                            अक्षदा, फुलं वाहावे. धूप दीप दाखवावा.खडी साखरेचा नैवेद्य दाखवून एक माळ ||श्री स्वामी समर्थ|| 
                            जप व एक माळ ||शि व चि दंबर|| जप करावा. 
                            परम पूज्य गुरुवर्यां चेस्मरण करून नमस्कार करावा अशा प्रकारे यंत्र सि द्ध होईल.
                            सूर्य यंत्र ज्या ठि काणी ठेवायला सांगि तले असेल त्या ठि काणी ठेवावे उदाहरणार्थ देवघरांमध्ये कि ंवा
                            दुकानांमध्ये सांगि तले असल्यास सांगि तलेल्या ठि काणीच ठेवावे.
            """
    sk33 = """ 
              सेवा ३३ : वाहन यंत्र स्थापना
                            गुरुवारी सकाळी यंत्र पाटावर ठेवून दोन-चार थेंब स्वच्छपाणी टाकून पुसून काढावे.यंत्र पाटावर ठेवून
                            अष्टगंध,अक्षदा, फुलं वाहावे. धूप दीप दाखवावा.खडी साखरेचा नैवेद्य दाखवून एक माळ ||श्री स्वामी समर्थ|| जप
                            व एक माळ ||शि व चि दंबर|| जप करावा. परम पूज्य गुरुवर्यां चेस्मरण करून नमस्कार करावा अशा प्रकारे यंत्र
                            सि द्ध होईल.त्यांनतर सांगि तलेल्या वाहनाला यंत्र लावावेत.
           """
    sk34 = """ 
              सेवा ३४ : वास्तू यंत्र स्थापना
                            गुरुवारी सकाळी यंत्र पाटावर ठेवून दोन-चार थेंब स्वच्छपाणी टाकून पुसून काढावेत्यानंतर यंत्र पाटावर ठेवून हळद,
                            कंु कू , अष्टगधं , अक्षदा, फु ल ं वाहावे. धपू दीप दाखवावा. त्यानतंर खडी साखरेचा नवै ेद्य दाखवनू एक माळ ||श्री
                            स्वामी समर्थ|| जप व एक माळ ||शि व चि दंबर|| जप करावा. 
                            परम पूज्य गुरुवर्यां चे स्मरण करून नमस्कार करावा अशा प्रकारे यंत्र सि द्ध होईल.वास्तू यंत्र ज्या दि शेला ठेवायला सांगि तले असेल त्या दि शेला ठेवावे.
           """
    sk35 = """ 
               सेवा ३५ : पंचमुखी हनुमान स्तोत्र वाचन सेवा.
                            शनि वारी
                            नित्योपासना पुस्तकामध्ये पंचमुखी हनुमान स्तोत्र दि ले आहेत.
                            स्तोत्र एकदा पूर्ण वाचून काढावे. वरील सेवा कि ती दि वस करायला सांगि तली आहे त्यानुसार करावी.
            """
    sk36 = """ 
                सेवा ३६ : हनुमान वडवानल स्तोत्र वाचन सेवा
                            पेलाभर पाणी समोर ठेऊन हनुमान वडवानल स्तोत्र वाचून काढावे त्यानंतर ते पाणी फुलाच्या साहाय्याने संपूर्ण
                            घरात, अगं णात, सर्वत्र शि पं डावे. अशाप्रकारे सतत तीन दि वस ही सेवा करावी.
            """
    sk37 = """ 
                सेवा ३७ : श्री लांगलू ास्त्र शत्रजंू य स्तोत्र वाचन सेवा
                            वरील स्तोत्र नि त्योपासना पस्ु तकात पान क्र. वर दि ले आहे. श्री लांगलू ास्त्र शत्रजंू य स्तोत्र मारोती मदिंरात जाऊन
                            कि ंवा घरी फोटो असल्यास फोटोसमोर एकदा वाचून काढावे.
                            वरील सेवा कि ती दि वस करायला सांगि तली आहे त्यानुसार करावी.
           """
    sk38 = """ 
                सेवा ३८ : कालभैरवाष्टक स्तोत्र वाचन सेवा
                            पाच अगरबत्त्या लावून कालभैरवाष्टक स्तोत्र वाचायला सुरुवात करावी.स्तोत्र वाचून झाल्यानंतर थोडा अंगारा
                            कपाळाला लावा व राहि लेला अगं ारा हातामध्ये घेऊन घरात चारही दि शले ा फंु कू न टाकावा. कालभरै वाष्टक
                            नि त्योपासना पुस्तकामध्ये पान क्र. वर दि ले आहे.
                            वरील सेवा कि ती दि वस करायला सांगि तली आहे त्यानुसार करावी.
            """
    sk39 = """ 
               सेवा ३९ : श्रीमहालक्ष्म्यांष्टकम स्तोत्र वाचन सेवा
                            श्रीमहालक्ष्म्यांष्टकम स्तोत्र एकदा पूर्ण वाचून काढावेत. वरील स्तोत्र नि त्योपासना पुस्तकात पान क्र......वर दि ले
                            आहे.
                            वरील सेवा कि ती दि वस करायला सांगि तली आहे त्यानुसार करावी.
             """
    sk40 = """
               सेवा ४० : व्यंकटेश स्तोत्र वाचन सेवा
                            श्री व्यंकटेश स्तोत्र नि त्योपासना पुस्तकात पान क्र.....वर दि ले आहे. हे स्तोत्र एकदा पूर्ण वाचून काढावे.
                            वरील सेवा कि ती दि वस करायला सांगि तली आहे त्यानुसार करावी.
           """

    sk41 = """ 
               सेवा ४१ : श्री सूक्त वाचन सेवा
                            श्री सूक्त नि त्योपासना पुस्तकात पान क्र....वर दि लेआहे.
                            श्री सूक्त एकदा पूर्ण वाचून काढावे.
               """

    sk42 = """ 
                सेवा ४२ : दर रवि वारी सूर्या ला जल देणे
                        रवि वारी सकाळी आंघोळ करून एका तांब्या मध्ये स्वच्छ पाणी घ्यावेत. सुर्या कडे पहात पाणी सोडावे व नमस्कार
                        करावा.
           """

    sk43 = """ 
                सेवा ४३ : महामत्ृ यजंु य कवच वाचन सेवा
                            पेलाभर पाणी घेऊन एक माळ ||शि व चि दंबर|| जप करावा. नंतर वरील कवच रोगी व्यक्तीच्या नाडीवर, हृदयावर
                            कि ंवा डोक्यावर हात ठेवून वाचावे. त्यानंतर ते तीर्थ रोगी व्यक्तीला तीन दि वस द्यावेत.
                            स्तोत्रामध्ये अमुक असा शब्द आला आहे.त्याशब्दाऐवजी रोगी व्यक्तीचे नाव घ्यावे.
           """

    sk44 = """  
                सेवा ४४ : अथर्व-वेदोक्त वल्गा सूक्त वाचन सेवा.
                            वरील स्तोत्र नि त्योपासना पुस्तकात पान क्र.... वर दि लेआहे.
                            स्त्रि यांनी डाव्या हाताच्या नाडीवर तीन बोटे ठेवून वल्गा सूक्त वाचावे.
                            पुरुषांनी उजव्या हाताच्या नाडीवर तीन बोटे ठेवून वल्गा सूक्त वाचावे.
                            सेवा स्त्री कि ंवा पुरुष ज्यांना सांगि तली असेल त्यांनीच करावी
           """

    sk45 = """ 
                सेवा ४५ : ललि ता सहस्त्रनाम वाचन सेवा.
                          रोगी व्यक्तीच्या छातीवर कि ंवा डोक्यावर हात ठेवून वरील स्तोत्र पूर्ण वाचून काढावेत.
           """
    sk46 = """ सेवा ४६ : रात्री सूक्त वाचन सेवा
                            रात्री सूक्त श्री दुर्गा सप्तशती पोथीमध्ये दि ले आहे. 
                            पेलाभर पाणी समोर ठेवून रात्रीसूक्त वाचून काढावे.
                            त्यानंतर रोगी व्यक्तीला ते तीर्थ प्यायला द्यावेत.
           """
    sk47 = """ सेवा ४७ : चक्षु स्तोत्र वाचन सेवा
                             वरील स्तोत्र नि त्योपासना पुस्तकात पान क्र..... वर दि ले आहे
           """
    sk48 = """ 
                सेवा ४८ : विष्णुसहस्त्रनाम वाचन सेवा
                           वरील स्तोत्र एकदा वाचावे. कि ती दि वस सांगि तले आहे त्यानुसार वाचायचे आहेत.
                           विष्णुसहस्त्रनाम रात्री वाचायला हरकत नाही.
                           एकदा वाचायला सांगि तले असल्यास एकदाच वाचावे.
           """
    sk49 = """ 
                सेवा ४९ : गायत्री सहस्त्रनाम वाचन सेवा
                             वरील स्तोत्र एकदा कि ंवा सांगि तले असेल ति तके दि वस सकाळी पूर्ण वाचून काढावेत
           """
    sk50 = """  
                 सेवा ५० : गणपती अथर्वशीर्ष वाचन सेवा
                             गणपती अथर्वशीर्ष नि त्योपासना पुस्तकात पान क्र.... वर दि ले आहे. सकाळी एकदा पूर्ण स्तोत्र वाचून काढावेत.
           """
    sk51 = """  
                  सेवा ५१ : रामरक्षा स्तोत्र वाचन सेवा
                            रामरक्षा स्तोत्र नि त्योपासना पुस्तकात पान क्र.... वर दि ले आहे. 
                            रामरक्षा एकदा वाचावी कि ंवा कि तीदा वाचायला सांगितली आहे त्यानुसार वाचायची आहेत.
                            
           """
    sk52 = """ 
                   सेवा ५२ : रुक्मि णी स्वयंवर वाचन सेवा
                               वरील सेवा कि तीदा वाचायला सांगि तले आहे त्यानुसार वाचून पूर्ण करावी."""
    sk53 = """ 
                   सेवा ५३ : वास्तुदोष नि वारण सेवा
                                वास्तुदोष नेमका कोणत्या दि शेला सांगि तला आहे त्यानसु ार भि तं ीवर पेंटने चेंडूच्या आकाराचे पाच ठि पके
                                एकरांगेत द्यावेत. दिशेनुसार रंग वापरावा..
                                अ. ईशान्य दि शा :-हि रवा रंग. ब. आग्नेय दि शा :-लाल रंग.
                                क. नैऋत्य दि शा :-लाल रंग. ड. वायव्य दि शा :-पांढरा रंग. 
           """
    sk54 = """ 
                   सेवा ५४ : नारायण नागबळी सेवा
                                वरील पूजा अंत्यत महत्वाची असून नाशि क जवळील त्रंबकेश्वरला जाऊन करावी लागते. ज्या सेवेकऱ्यांना परम
                                पूज्य गुरुवर्यां नी नारायण नागबळी सांगि तली आहे त्यांनीच करायची आहे.
                                वरील पूजेच्या वि शि ष्ट तारखा असतात त्यासंदर्भा तील व अधि क माहि ती संबंधि त सेवेकऱ्यांकडून घ्यायची आहे.
            """
    sk55 = """
     
                  सेवा ५५  : मंगळ यंत्र व मारुती यंत्र स्थापना
                                मंगळवारी दुपारी बाराच्या सुमारास दोन्हीही यंत्रावर दोन-चार थेंब स्वच्छ पाणी टाकून पुसून काढावे नंतर पाटावर
                                ठेवून अष्टगंध,अक्षता,फूल वाहावे. धूपदीप दाखवावा.खडीसाखरेचा नैवेद्द दाखवावा. त्यानंतर एक माळ ||श्री
                                स्वामी समर्थ|| व एक माळ ||शि व चि दंबर|| जप करावा.
                                गुरुवर्यां चेस्मरण करून नमस्कार करावा अशा प्रकारे यंत्र सि द्ध होईल.
                                मंगळ यंत्र देवघरात ठेवून दररोज त्यावर अष्टगधं, फुले वाहून यंत्राचे पूजन करावे.
                                 व मारुती यंत्र घराच्या ईशान्येला फूटभर खड्डा करून पुरवून द्यावे,खड्डा करणे शक्य नसल्यास ईशान्य दि शेला छताच्या 
                                अगदी जवळ कुणाचाही हात लागणार नाही इतक्या उंचीवर एक पाटी ठोकून त्यावर लाल कापड टाकून यंत्र ठेऊन द्यावे. 
                                ईशान्य दि शेला सज्जा असल्यास त्यावर यंत्र ठेवावे. पूजन करण्याआधी यंत्राला लॅमि नेशन करून घ्यावे..
                    टीप :- मारुती यंत्राची स्थापना पुरुषांच्या हातूनच कारवी.
                    
             """

    sk56 = """ 
                  सेवा ५६ : दि वा लावणे
                                आठवड्यातून एखाद्या दि वशी गायीच्या तुपाचा दि वा कि ंवा ति ळाच्या तेलाचा दि वा जो सांगि तला असेल तो
                                देवघरात लावावा.
          """
    sk57 = """  
                  सेवा ५७  : गोमूत्र अर्क घेणे
                                 आरोग्य वि षयक समस्येकरीता गोमूत्र अर्क अत्यंत महत्वाचेआहे. 
                                 एक चमचा गोमूत्र अर्क एक कप पाण्यात सकाळी उपाशी पोटी घ्यायचे आहे त्यानंतर अर्धा तास काहीच खाऊ अथवा पि ऊ नये.
                                 टीप :-शुद्ध केलेले गोमूत्र अर्क मार्केट मध्ये मि ळेल. एक बाटली पूर्ण संपेपर्यंत घ्यायची आहे
           """
    sk58 = """ 
                 सेवा ५८ : एक चमचा कडुलि बं ाच्या पानाचा रस एक कप पाण्यात तीन दि वस घ्यायचा आहे.
           """
    sk59 = """  
                 सेवा ५९ : कुलदेवीची टाक/फोटो/मूर्ती वरील हळद
                                घरी तयार केलेली हळद एका वाटी मध्ये घ्यावी. त्यांनतर श्री सूक्त वाचायला सुरवात करावी. 
                                प्रत्येक दोन ओळी वाचून झाल्याकी पाचही बोटांनी चि मूटभर हळद कुलदेवीची टाक कि ंवा फोट कि ंवा मूर्ती वर वाहायची आहे.
                                अशाप्रकारे श्री सूक्ताच्या प्रत्येक दोन ओळी वाचून झाल्या की हळद वाहायची आहे. 
                                त्यानंतर वाहलेली हळद तीन दिवस दुधात कि ंवा मधात कि ंवा पाण्यात टाकून घ्यायची आहे. 
                                श्री सूक्त नि त्योपासना पुस्तकात पान क्र..... वर दिले आहे.
           """
    sk60 = """  
                 सेवा ६० : एका चमच्यामध्ये थोडे सहद घ्या. चमचातील सहदाकडे पाहत 11 वेळा || श्री स्वामी समर्थ || व 11 वेळा || शि व
                          चिदंबर || जप करावा त्यानंतर ते सहद खाऊन घ्यावेत.
           """
    sk61 = """ 
                सेवा ६१ : कंु कू मार्चन करून कपाळाला कंु कू लावणे
                                एका वाटीमध्ये थोड े कंु कू घेऊन देवी च्या फोटो समोर कि ं वा मर्तीू समोर श्रीसक्ू त वाचायला सरुु वात करा. 
                                दोन ओळी वाचनू पर्णू झाल्याकी पाचही बोटाने कंु कू देवीच्या फोटोवर कि ं वा मर्तीू वर वाहावे,परत दसु ऱ्या दोन ओळी वाचाव्यात
                                पन्ु हा पाचही बोटाने कंु कू वाहावेत अशा प्रकारे श्रीसक्ु ताच्या प्रत्येक दोन ओळीनतं र देवीला कंु कू वहायचे
                                आहेत.
                                श्रीसक्ू त पर्णु वाचनू झाल्यानतं र वाहि लेले कंु कू एका डबीमध्ये भरून ठेवावे व रोज आपल्या पतीचे ध्यान
                                करून कंु कू कपाळाला लावायचे आहे.आणि कु लदेवीला मि स्टरांकरि ता वि नतं ी करायची आहे.श्रीसक्ू त नि त्योपासना
                                पुस्तकांमध्ये पान क्र..... वर दिले आहेत.
            """
    sk62 = """ 
                सेवा ६२ : पक्षांना तांदूळ/पाणी ठेवणे
                            शुक्रवारी सकाळी एका प्लेटमध्ये थोडेसे तांदूळ घेऊन पक्षाला खायला ठेवावेत.
                            शनि वारी प्लेटमध्ये शिल्लक राहि लेल्या तांदुळात घरचे थोडे तांदूळ टाकून भात करावा.
                            तो भात फक्त रोगी व्यक्तीला कि ंवा ज्यांना खायला सांगितला असेल त्यानांच द्यायचा आहे.
           """
    sk63 = """ 
                 सेवा ६३  : देवघरात जप युनि ट लावणे
                             जप युनि ट मध्ये वेगवेगळ्या देवतांचे मंत्र रेकॉर्ड केलेलेअसतात त्यापैकी || श्री स्वामी समर्थ || मंत्र देवघरात नेहमी
                             चालू ठेवावा.
           """
    sk64 = """ 
                 सेवा ६४  : देवघर कि ंवा देव्हारा मध्ये काही अडचणी सांगि तल्या असतील तर गुरुआज्ञेनुसार संपर्का तील
                           जबाबदार सेवेकरी कडून तपासून घ्यावेत.
            """
    sk65 = """
                 सेवा ६५  : गोशाळा सेवा
                            गोशाळेला पैसे देण्याऐवजी वर्षा तून कि मान एकदा तरी गोमातेकरीता चारा द्यावा.
           """
    sk66 = """  
                 सेवा ६६ : अन्नदान सेवा
                            अन्नदान करणे ही खपू पण्ंु याची सेवा आहे. 
                            वर्षातनू एकदा यथाशक्ती अन्नदान करावे कि ं वा कि मान पाच लहान मुलांना तरी जेवू घालावेत.
               """
    sk67 = """ 
                 सेवा ६७ : दहीभात उतारा
                            शुक्रवारी दुपारी बारावाजता एका पत्रावळीवर बि न मि ठाचा भात व दही घेऊन ज्या व्यक्तीचा उतारा काढायचा आहे
                            त्या व्यक्तीला पूर्वेकडे तोंड करून बसवावे.पत्रावळी हातात घेऊन व्यक्तीच्या डोक्यावरून खाली याप्रमाणेसात वेळा
                            'L' आकारामध्ये उतारा काढावा. पत्रावळी व्यक्तीला लागणार नाही याची काळजी घ्यावी. 
                            त्यानंतर तो दहीभात घराच्या बाहेर एका बाजूला ज्या ठि काणी कुणाचाही पाय पडणार नाही अशा ठि काणी टाकून द्यावा. 
                            नंतर पाय धुऊन गुळण्या करूनच घरामध्ये प्रवेश करावा.
           """
    sk68 = """ """
    sk69 = """
     
                 सेवा ६९ : नारळ उतारा
                            ज्या व्यक्तीचा उतारा काढायचा आहे त्याला पूर्वेकडेतोंड करून बसावावे. उतारा काढणाऱ्या व्यक्तीने नारळाची
                            शेंडी वर राहील या पद्धतीने नारळ हातात घेऊन सात वेळा 'L' आकारांमधे बसलेल्या व्यक्तीच्या अंगावरून
                            (डोक्यावरून खाली) याप्रमाणे सात वेळा 'L' आकारामध्येउतारा काढावा.
                            एका बाजूला नारळ फोडून ठि काणी टाकून द्यावे. वाहन कि ंवा घराचा उतारा काढायला सांगि तले असल्यास 
                            वरील पद्धतीनेच काढावा.ही क्रिया शनिवारी कि ंवा अमावसेला करायची आहे.
            """
    sk70 = """ 
                सेवा ७० : आसरांची सेवा
                            ही सेवा फक्त महि लांनीच करायची आहे.एका शुक्रवारी दुपारी बाराच्या सुमारास एका द्रोणात बि ना मि ठाचा भात व
                            दही घ्यावे. एका पत्रावळीवर ओटीचे साहि त्य घ्यावे हळद-कंु कू ,खारीक, बदाम, हि रव्या बांगड्या, सपु ारी,
                            हळकंु ड,खोबरे, एक रुपयाचा कलदार व तांदळू घेऊन पजू ा करून वाहत्या पाण्यात सोडून द्यावे. 
                            कि ं वा ज्या ठि काणी स्थापि त आसरा देवीचे मंदि र आहे त्या ठि काणी पूजा करून वरील साहि त्य ठेवून द्यावे. 
                            घरामध्ये हात पाय धुऊन प्रवेश करावा.
           """
    sk71 = """ 
                सेवा ७१ : पांढऱ्या मोहरीची सेवा.
                            शनि वारी कि ंवा अमावसेला उजव्या हातामध्ये थोडी पांढरी मोहरी घेऊन एक वेळा कालभैरवाष्टक व एक वेळा
                            वल्गा सुक्त वाचावे त्यानंतर घरामध्ये,शेतामध्ये कि ंवा प्लॉटमध्ये कि ंवा ज्या ठि काणी टाकायला सांगितले असेल
                            त्या ठि काणी सर्व दि शेने 2-2 दाणे टाकून द्यावे.
                            टीप -कालभैरवाष्टक व वल्गा सूक्त नि त्योपासना पुस्तकात दि ले आहे.
           """
    sk72 = """ 
                सेवा ७२ : मारोती मंदि रात दि व्यात तेल टाकणे (१ शनिवारी ३ शनिवारी)
                            शनि वारी एका मातीच्या पणती मध्ये थोडे तेल घ्या. पणती हातामध्ये घेऊन तेलामध्ये पहात एक माळ 
                            ||श्री स्वामी समर्थ || व एक माळ || शिव चि दंबर || हा जप करावा.
                            त्यानंतर घराजवळील मारुती मंदि रामध्ये जाऊन जळत असलेल्या दि व्यांमध्ये तेल टाकून नमस्कार करून परत यावे.
                            मंदि रामध्ये दि वा जळत नसल्यास स्वतःदिवा लावावा. 
                            अशा प्रकारे एक शनि वार सांगि तला असल्यास एक वेळा कि ंवा तीन शनिवार सांगितले असल्यास
                            तीन वेळा वरील क्रि या करायची आहे.
                            टीप :-वरील सेवा पुरुषांच्या हातूनच करायची आहे.
            """
    sk72_1 = """ 
    
               सेवा ७२_१ मारोती मंदि रात दि व्यात तेल टाकणे (३ शनिवारी)
                            शनि वारी एका मातीच्या पणती मध्ये थोडे तेल घ्या. पणती हातामध्ये घेऊन तेलामध्ये पहात एक माळ ||श्री
                            स्वामी समर्थ || व एक माळ || शि व चि दंबर || हा जप करावा.
                            त्यानंतर घराजवळील मारुती मंदि रामध्ये जाऊन जळत असलेल्या दि व्यांमध्ये तेल टाकून नमस्कार करून परत यावे. 
                            मंदिरामध्ये दि वा जळत नसल्यास स्वतः दिवा लावावा. 
                            अशा प्रकारे एक शनि वार सांगि तला असल्यास एक वेळा कि ंवा तीन शनि वार सांगि तले असल्यास
                            तीन वेळा वरील क्रि या करायची आहे.
                            टीप :-वरील सेवा पुरुषांच्या हातूनच करायची आहे.
              """

    sk73 = """ 
                सेवा ७३ : शनि मंदि रात तेल टाकणे
                      शनि वारी एका मातीच्या पणती मध्ये थोडे तेल घ्या. पणती हातामध्ये घेऊन तेलामध्ये पहात एक माळ
                     ||श्री स्वामी समर्थ || व एक माळ || शि व चि दंबर || हा जप करावा.
                     त्यानंतर ते तेल शनी मंदि रातजाऊन टाकून द्यावे.अशा प्रकारे एक शनि वार सांगितला असल्यास 
                     एक वेळा कि ंवा तीन शनि वार सांगि तले असल्यास तीन वेळा वरील क्रिया करायची आहे.
           """


    if seva == 'sk6':
        seva_details = sk6
        seva = dic1[seva]
    elif seva == 'sk7':
        seva_details = sk7
        seva = dic1[seva]
    elif seva == 'sk8':
        seva_details = sk8
        seva = dic1[seva]
    elif seva == 'sk9':
        seva_details = sk9
        seva = dic1[seva]
    elif seva == 'sk10':
        seva_details = sk10
        seva = dic1[seva]
    elif seva == 'sk11':
        seva_details = sk11
        seva = dic1[seva]
    elif seva == 'sk12':
        seva_details = sk12
        seva = dic1[seva]
    elif seva == 'sk13':
        seva_details = sk13
        seva = dic1[seva]
    elif seva == 'sk14':
        seva_details = sk14
        seva = dic1[seva]
    elif seva == 'sk15':
        seva_details = sk15
        seva = dic1[seva]
    elif seva == 'sk16':
        seva_details = sk16
        seva = dic1[seva]
    elif seva == 'sk16_1':
        seva_details = sk16_1
        seva = dic1[seva]
    elif seva == 'sk17':
        seva_details = sk17
        seva = dic1[seva]
    elif seva == 'sk17_1':
        seva_details = sk17_1
        seva = dic1[seva]
    elif seva == 'sk18':
        seva_details = sk18
        seva = dic1[seva]
    elif seva == 'sk19':
        seva_details = sk19
        seva = dic1[seva]
    elif seva == 'sk20':
        seva_details = sk20
        seva = dic1[seva]
    elif seva == 'sk21':
        seva_details = sk21
        seva = dic1[seva]
    elif seva == 'sk21_1':
        seva_details = sk21
        seva = dic1[seva]
    elif seva == 'sk22':
        seva_details = sk22
        seva = dic1[seva]
    elif seva == 'sk22_1':
        seva_details = sk22
        seva = dic1[seva]
    elif seva == 'sk23':
        seva_details = sk23
        seva = dic1[seva]
    elif seva == 'sk23_1':
        seva_details = sk23
        seva = dic1[seva]
    elif seva == 'sk24':
        seva_details = sk24
        seva = dic1[seva]
    elif seva == 'sk25':
        seva_details = sk25
        seva = dic1[seva]
    elif seva == 'sk26':
        seva_details = sk26
        seva = dic1[seva]
    elif seva == 'sk27':
        seva_details = sk27
        seva = dic1[seva]
    elif seva == 'sk27_1':
        seva_details = sk27
        seva = dic1[seva]
    elif seva == 'sk27_2':
        seva_details = sk27_2
        seva = dic1[seva]
    elif seva == 'sk28':
        seva_details = sk28
        seva = dic1[seva]
    elif seva == 'sk29':
        seva_details = sk29
        seva = dic1[seva]
    elif seva == 'sk30':
        seva_details = sk30
        seva = dic1[seva]
    elif seva == 'sk31':
        seva_details = sk31
        seva = dic1[seva]
    elif seva == 'sk32':
        seva_details = sk32
        seva = dic1[seva]
    elif seva == 'sk33':
        seva_details = sk33
        seva = dic1[seva]
    elif seva == 'sk34':
        seva_details = sk34
        seva = dic1[seva]
    elif seva == 'sk35':
        seva_details = sk35
        seva = dic1[seva]
    elif seva == 'sk36':
        seva_details = sk36
        seva = dic1[seva]
    elif seva == 'sk37':
        seva_details = sk37
        seva = dic1[seva]
    elif seva == 'sk38':
        seva_details = sk38
        seva = dic1[seva]
    elif seva == 'sk39':
        seva_details = sk39
        seva = dic1[seva]
    elif seva == 'sk40':
        seva_details = sk40
        seva = dic1[seva]
    elif seva == 'sk41':
        seva_details = sk41
        seva = dic1[seva]
    elif seva == 'sk42':
        seva_details = sk42
        seva = dic1[seva]
    elif seva == 'sk43':
        seva_details = sk43
        seva = dic1[seva]
    elif seva == 'sk44':
        seva_details = sk44
        seva = dic1[seva]
    elif seva == 'sk45':
        seva_details = sk45
        seva = dic1[seva]
    elif seva == 'sk46':
        seva_details = sk46
        seva = dic1[seva]
    elif seva == 'sk47':
        seva_details = sk47
        seva = dic1[seva]
    elif seva == 'sk48':
        seva_details = sk48
        seva = dic1[seva]
    elif seva == 'sk49':
        seva_details = sk49
        seva = dic1[seva]
    elif seva == 'sk50':
        seva_details = sk50
        seva = dic1[seva]
    elif seva == 'sk51':
        seva_details = sk51
        seva = dic1[seva]
    elif seva == 'sk52':
        seva_details = sk52
        seva = dic1[seva]
    elif seva == 'sk53':
        seva_details = sk53
        seva = dic1[seva]
    elif seva == 'sk54':
        seva_details = sk54
        seva = dic1[seva]
    elif seva == 'sk55':
        seva_details = sk55
        seva = dic1[seva]
    elif seva == 'sk56':
        seva_details = sk56
        seva = dic1[seva]
    elif seva == 'sk57':
        seva_details = sk57
        seva = dic1[seva]
    elif seva == 'sk58':
        seva_details = sk58
        seva = dic1[seva]
    elif seva == 'sk59':
        seva_details = sk59
        seva = dic1[seva]
    elif seva == 'sk60':
        seva_details = sk60
        seva = dic1[seva]
    elif seva == 'sk61':
        seva_details = sk61
        seva = dic1[seva]
    elif seva == 'sk62':
        seva_details = sk62
        seva = dic1[seva]
    elif seva == 'sk63':
        seva_details = sk63
        seva = dic1[seva]
    elif seva == 'sk64':
        seva_details = sk64
        seva = dic1[seva]
    elif seva == 'sk65':
        seva_details = sk65
        seva = dic1[seva]
    elif seva == 'sk66':
        seva_details = sk66
        seva = dic1[seva]
    elif seva == 'sk67':
        seva_details = sk67
        seva = dic1[seva]
    elif seva == 'sk68':
        seva_details = sk68
        seva = dic1[seva]
    elif seva == 'sk69':
        seva_details = sk69
        seva = dic1[seva]
    elif seva == 'sk70':
        seva_details = sk70
        seva = dic1[seva]
    elif seva == 'sk71':
        seva_details = sk71
        seva = dic1[seva]
    elif seva == 'sk72':
        seva_details = sk72
        seva = dic1[seva]
    elif seva == 'sk72_1':
        seva_details = sk72_1
        seva = dic1[seva]
    elif seva == 'sk73':
        seva_details = sk73
        seva = dic1[seva]

    values = {'seva_descrption':seva_details,'seva_fullform':seva}
    return values




