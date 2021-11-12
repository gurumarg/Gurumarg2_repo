
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from .models import sampark_sevekari, session_data,seva_data
import random
from datetime import date
#recode = '1234'
#g_email1 = ''



# Create your views here.


def question_form(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    return render(request, 'question_form.html', {'user_details': user_details})


def return_to_home(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    type =user_details.type
    if type == 'main_admin':
        return render(request,'home_admin.html', {'user_details': user_details})
    if type == 'sampark_sevekari':
        return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
    if type == 'verified' or type == 'unverified':
        return render(request,'home_prashankarta.html',{'user_details': user_details})

def new_question(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    function1 = 'new question'
    return render(request, 'question_form.html', {'user_details': user_details,'function1':function1})

def repeat_question(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    button1= request.POST['b1']
    user_questions = session_data.objects.filter(User_id_id=id)
    if user_questions:
        if button1 == 'b1':
             function2 = 'repeat question'
        else:
              function2 = 'repeat question data'
        return render(request, 'question_form.html', {'user_details': user_details, 'function2': function2,'data':user_questions})
    else:
        messages.info(request,"तुम्ही प्रश्न अजून केलेले नाहीत ")
        return render(request,'question_form.html', {'user_details': user_details})


def submit_repeat_question(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    session_id = request.POST['select_questions']
    print('session_id is : ',session_id)
    if session_id :
        record = session_data.objects.get(pk=session_id)
        print('record details are : ',record)
        record.Date_filled = str(record.Date_filled) + ' / '+ str(date.today())
        record.status = 'submitted'
        record.save()
        messages.info(request,' ✅ तुमचे जुने प्रश्न पुन्हा स्वीकारण्यात आले आहेत.  ✅ ')
    return render(request,'question_form.html', {'user_details': user_details})


def save_prashan(request):

    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    slct1 = request.POST['slct1']
    slct2 = request.POST['slct2']
    text1 = request.POST['text1']
    slct3 = request.POST['slct3']
    slct4 = request.POST['slct4']
    text2 = request.POST['text2']
    flag1 = ''
    flag2 = ''
    p1 = ''
    p2 = ''
    dict = {'g1':'आर्थिक प्रगती','g2':'व्यवसायात यश मिळेल का?','g3':'नौकरीयोग','g4':'शेतात उत्पन्न कमी','g5':'जनावरांच्या व्याधीबाबत',
              'g6':'शिक्षणात प्रगती','g7':'स्वतःच्या घराचे योग','g8':' विवाहयोग ','g9':'संतानप्राप्ती योग','g10':'विवाहीता असुन माहेरी राहते सासरी परत नेतील का?',
               'g11':'कोर्टकचेरी अनुकुलता','g12':'आध्यात्मिक प्रगती होणेबाबत','g13':'आरोग्य विषयक','g14':'घरात अशांतता','g15':'कुलदेवीबाबत माहीती नाही',
                'g16':'बाहेरबाधेचा त्रास','g17':'इतर'}
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    type = user_details.type
    print('text data : ', text1)
    print('slct1 data is:',slct1)
    if slct1:
        if slct1 == 'g1' or slct1 == 'g3' or slct1 == 'g6' or slct1 == 'g7' or slct1 == 'g8' or slct1 == 'g9' or slct1 == 'g11' or slct1 == 'g12' or slct1 == 'g13' :
                print('i am 1st condition')
                if slct2:
                   p1 = dict[slct1] + '/ ' + slct2
                   flag1 = 'done'

                else:
                     messages.info(request, 'प्रश्न १:प्रश्नाच्या स्वरूपावरून पुढील निवड करावी 2nd half is missing')

        if slct1 == 'g2' or slct1 == 'g17' or slct1 == 'g5':

                if len(text1) > 1:
                      p1 = dict[slct1] + ','+ text1
                      flag1 = 'done'
                else:
                       messages.error(request,'प्रश्न १:अधिक माहिती द्या ')

        if slct1 == 'g4' or slct1 == 'g10' or slct1 == 'g14' or slct1 == 'g15' or slct1 == 'g16':
                p1 = dict[slct1]
                flag1 = 'done'

    else:
            messages.error(request,'प्रश्न १:आपल्या प्रश्नाचे स्वरुप पुढीलपैकी निवडावे')

    if slct3 == '':
       p2 = None
       flag2 = 'done'
    else:
        if slct3 in [ 'g1', 'g3', 'g6', 'g7', 'g8', 'g9', 'g11', 'g12', 'g13'] :
             if slct4 :
               p2 = dict[slct3] + '/ ' + slct4
               flag2 = 'done'
             else:
                 messages.error(request, 'प्रश्न २: प्रश्नाच्या स्वरूपावरून पुढील निवड करावी ')
        elif slct3 in ['g4','g10','g14','g15','g16']:
               p2 = dict[slct3]
               flag2 = 'done'
        elif slct3 in ['g2', 'g5','g17']:
               if len(text2) > 1:
                  p2 = dict[slct3] + '/'+ text2
                  flag2 = 'done'
               else:
                   messages.error(request,'प्रश्न २: अधिक माहिती द्या ')
    if (flag1 == 'done') and (flag2 == 'done'):
       qa = session_data(User_id_id = id,prashan1 = p1, prashan2 = p2)
       qa.save()
       messages.info(request,' ✅ आपले प्रश्न स्वीकारण्यात आले आहेत.  ✅ ' )

       type = user_details.type
       if type == 'sampark_sevekari':
            return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
       elif type == 'main_admin':
            return render(request, 'home_admin.html', {'user_details': user_details})
       elif type == ('unverified') or ('verified'):
            return render(request, 'home_prashankarta.html', {'user_details': user_details})

    else:
        return render(request, 'question_form.html', {'user_details': user_details})

def profile_manage(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    function1 = 'profilepage'
    if user_details.type == 'sampark_sevekari':
        sscode = sampark_sevekari.objects.get(User_id_id=id)

        return render(request, 'profilepage.html',{'user_details': user_details, 'sscode': sscode,'function1':function1})
    elif user_details.type == 'main_admin':
        sscode = sampark_sevekari.objects.get(User_id_id=id)

        return render(request, 'profilepage.html',{'user_details': user_details, 'sscode': sscode,'function1':function1})
    else:
        sscode = 'None'

        return render(request, 'profilepage.html',{'user_details': user_details, 'sscode': sscode,'function1':function1})

def profile_update(request):
    #global recode, g_email1
    recode = '1234'
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    city = request.POST['city']
    code2 = request.POST['wmcode']
    mobile2 = request.POST['w_mobile']
    g_email1 = request.POST['email']
    user_details.city = city
    user_details.code2 = code2
    if mobile2 != user_details.mobile2:
        if not (len(mobile2)==0):
            if not ((len(mobile2) == 10) and (mobile2.isnumeric())):
                messages.info(request, '⚠ अपूर्ण मोबाईल नंबर किंवा  मोबाईल  नंबर  संख्येत अपेक्षित आहे , पुन्हा प्रोफाइल वर क्लिक करून अपडेट करा  ⚠️')
                return render(request, 'profilepage.html', {'user_details': user_details})
    user_details.mobile2 = mobile2
    if user_details.email == g_email1:
        user_details.save()
        messages.info(request,'👍प्रोफाइल  अपडेटेड 👍')
        if user_details.type == 'main_admin':
            return render(request, 'home_admin.html', {'user_details': user_details})
        elif user_details.type == 'sampark_sevekari':
            return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
        else:
            return render(request, 'home_prashankarta.html', {'user_details': user_details})
    else:
           user_details.save()
           recode = random.randrange(1000, 9999)
           recode_m = recode + 135
           recode = str(recode)
           print(recode)
           msg = 'नोंदणीसाठी तुमचा व्हेरीफिकेशन  कोड :' + recode + ' हा राहील '
           send_mail('Email Verification', msg, 'samarthview@gmail.com',[g_email1, 'gurumargdarshan14@gmail.com'], fail_silently=True)

           messages.info(request,'📧 तुमच्या  ई-मेल वर  कोड पाठविण्यात आला आहे , १ मिनिट  थांबा ,\n  कोड नाही आला तर तुम्ही दिलेला ई-मेल बरोबर आहे , ते पहा 📧 ')
           function2 = 'verify_email'
           dic = {'g_email1':g_email1,'recode_m':recode_m}
           return render(request, 'profilepage.html', {'user_details': user_details, 'function2':function2,'dic':dic})


def verify_recode(request):
    g_email1 = request.POST['email']
    recode = int(request.POST['recode_m'])
    recode = str(recode - 135)

    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    #global recode,g_email1
    ecode = request.POST['ecode']
    if ecode == recode:
        user_details.email = g_email1
        user_details.save()
        messages.info(request, ' ✅ ई-मेल अपडेटेड कम्प्लिटेड  ✅ ')
        type = user_details.type
        if type == 'sampark_sevekari':
            return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
        elif type == 'main_admin':
            return render(request, 'home_admin.html', {'user_details': user_details})
        elif type == ('unverified') or ('verified'):
            return render(request, 'home_prashankarta.html', {'user_details': user_details})

    else:
        messages.info(request, '❌ ई-मेल कोड चुकीचा आहे ,पुन्हा प्रयत्न करा ❌')
        function2 = 'verify_email'
        recode = int(recode)
        recode_m = recode + 135
        dic = {'recode_m': recode_m, 'g_email1': g_email1}
        return render(request, 'profilepage.html', {'user_details': user_details, 'function2': function2,'dic':dic})

# approving new user by sampark sevekari

def approve_kara(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    sscode = sampark_sevekari.objects.get(User_id_id=id)
    unvdata = get_user_model().objects.filter(sscode=sscode.sscode).filter(type='unverified')
    if unvdata:
        return render(request, 'approvepage.html',{'user_details': user_details, 'unvdata': unvdata})
    else:
        if user_details.type == 'sampark_sevekari':
            messages.info(request,'अप्रूव्ह करण्या करिता विनंती नाही आहे ')
            return render(request,'home_sampark_sevekari.html',{'user_details': user_details})
        elif user_details.type == 'main_admin':
            messages.info(request, 'अप्रूव्ह करण्या करिता विनंती नाही आहे ')
            return render(request, 'home_admin.html', {'user_details': user_details})


def modify_user_type(request):
    pid = request.POST['select_name']
    utype = request.POST['type']
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)


    if utype == 'verified':
      record =  get_user_model().objects.get(pk=pid)
      record.type= "verified"
      record.save()
      sampark_sevekari.objects.filter(User_id_id=pid).update(status = 'inactive')

    elif utype =='Rejected':
        record = get_user_model().objects.get(pk=pid)
        record.type = "Rejected"
        record.save()

    elif utype == 'main_admin':
        record = get_user_model().objects.get(pk=pid)
        record.type = "main_admin"
        record.save()
    elif utype == 'sampark_sevekari':
        msg1=add_sampark_sevekari(pid)
        messages.info(request, msg1)

    utype = user_details.type
    if utype == 'sampark_sevekari':
                return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
    elif utype == 'main_admin':
                return render(request, 'home_admin.html', {'user_details': user_details})


def add_sampark_sevekari(pid):
    userid = pid
    new_sscode = 'ss' + str(random.randrange(100, 999))
    record = get_user_model().objects.get(pk=userid)
    allsevekari = sampark_sevekari.objects.all()
    check = 'not_present'
    for i in allsevekari:
        print('type of i.user_id_id:',type(i.User_id_id))
        if i.User_id_id == int(userid):
            print("Sampark sevekari exist")
            ss_old = sampark_sevekari.objects.get(User_id_id = userid)
            ss_old.status = 'active'
            ss_old.save()
            record.type = "sampark_sevekari"
            record.save()
            name = record.first_name + ' ' + record.last_name
            msg1 = name + ' ' + 'यांना संपर्क सेवेकरी म्हणून अ‍ॅड करण्यात आले आहे '
            msg = 'तुमचा सम्पर्क सेवेकरी कोड हा आहे:' + ss_old.sscode
            send_mail('Selected As Sampark Sevekari', msg, 'samarthview@gmail.com', [record.email], fail_silently=True)
            return msg1
        if  i.sscode == new_sscode:
               check = 'present'
    if check == 'not_present':
        ss = sampark_sevekari(User_id_id=userid, sscode=new_sscode)
        ss.save()
        msg = 'तुमचा सम्पर्क सेवेकरी कोड हा आहे:' + new_sscode
        record.type = "sampark_sevekari"
        record.save()
        send_mail('Selected As Sampark Sevekari', msg, 'samarthview@gmail.com', [record.email], fail_silently=True)
    else :
        userid = userid
        add_sampark_sevekari(userid)


def select_question_seva(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    id = int(id)
    pk_table = session_data.objects.filter(User_id_id = id)
    function1 = 'display questions'
    return render(request,'view_sevapage.html',{'user_details':user_details,'pk_table':pk_table, 'function1':function1})



def view_seva(request):
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
    else:
        function2 = 'multiple_seva_id'

    return render(request, 'view_sevapage.html',{'user_details': user_details,'dic1':dic1,'sd':sevadic,'function2': function2,'session_id':session_id})


def view_selectedsevaid(request):
    id = request.POST['user']
    user_details = get_user_model().objects.get(pk=id)
    seva_id = request.POST['seva_id']
    session_id = request.POST['session_id']
    dic1 = prashandetails(session_id)
    sevadetails = seva_data.objects.get(seva_id = seva_id)
    sevadic = make_seva_dic(sevadetails)
    print('sevadic return value',sevadic)
    function2 = 'user_seva_display'
    return render(request, 'view_sevapage.html',
                  {'user_details': user_details, 'dic1': dic1, 'sd': sevadic, 'function2': function2})


def prashandetails(session_id):
    session_id = session_id
    userdata = session_data.objects.get(pk=session_id)
    prashan1 = userdata.prashan1
    prashan2 = userdata.prashan2
    pid = userdata.User_id_id
    prashankarta_name = get_user_model().objects.get(pk=pid)
    full_name = prashankarta_name.first_name + ' ' + prashankarta_name.last_name
    dic1 = {'prashan1': prashan1, 'prashan2': prashan2, 'pname': full_name}
    return dic1



def make_seva_dic(sevadetails1):
    sevadetails = sevadetails1
    print('sevatails in funxtion :',sevadetails)
    sevadic = {'seva_id' : sevadetails.seva_id, 'date_qa':sevadetails.date_qa,'seva_status':sevadetails.seva_status,
               'anubhav':sevadetails.anubhav,'sahitya':sevadetails.sahitya,'seva_explained':sevadetails.seva_explained,
               'guru_ans_p1':sevadetails.guru_ans_p1,'guru_ans_p2':sevadetails.guru_ans_p2,
               'session_id_id':sevadetails.session_id_id,'user_id_id':sevadetails.user_id_id}

    if  len(sevadetails.seva1) > 1 :
        sevadic['seva1']=sevadetails.seva1
        sevadic['status1'] = sevadetails.status1
        print('sevadeatils from list:',sevadetails.status1)
    if  len(sevadetails.seva2) > 1:
        sevadic['seva2']=sevadetails.seva2
        sevadic['status2'] = sevadetails.status2
    if len(sevadetails.seva3) > 1:
        sevadic['seva3']=sevadetails.seva3
        sevadic['status3'] = sevadetails.status3
    if len(sevadetails.seva4) > 1:
        sevadic['seva4']=sevadetails.seva4
        sevadic['status4'] = sevadetails.status4
    if len(sevadetails.seva5) > 1:
        sevadic['seva5']=sevadetails.seva5
        sevadic['status5'] = sevadetails.status5
    if  len(sevadetails.seva6) > 1:
        sevadic['seva6']=sevadetails.seva6
        sevadic['status6'] = sevadetails.status6
    if len(sevadetails.seva7) > 1:
        sevadic['seva7']=sevadetails.seva7
        sevadic['status7'] = sevadetails.status7
    if len(sevadetails.seva8) > 1:
        sevadic['seva8']=sevadetails.seva8
        sevadic['status8'] = sevadetails.status8
    if len(sevadetails.seva9) > 1:
        sevadic['seva9']=sevadetails.seva9
        sevadic['status9'] = sevadetails.status9
    if len(sevadetails.seva10) > 1 :
        sevadic['seva10']=sevadetails.seva10
        sevadic['status10'] = sevadetails.status10
    if len(sevadetails.seva11) > 1:
        sevadic['seva11']=sevadetails.seva11
        sevadic['status11'] = sevadetails.status11
    if len(sevadetails.seva12) > 1:
        sevadic['seva12']=sevadetails.seva12
        sevadic['status12'] = sevadetails.status12
    if len(sevadetails.seva13) > 1 :
        sevadic['seva13']=sevadetails.seva13
        sevadic['status13'] = sevadetails.status13
    if len(sevadetails.seva14) > 1:
        sevadic['seva14']=sevadetails.seva14
        sevadic['status14'] = sevadetails.status14
    if len(sevadetails.seva15) > 1:
        sevadic['seva15']=sevadetails.seva15
        sevadic['status15'] = sevadetails.status15

    return sevadic


def update_seva(request):
    seva_id = request.POST['seva_id']
    anubhav = request.POST['anubhav_status']
    status1 = request.POST['sevastatus1']
    status2 = request.POST['sevastatus2']
    status3 = request.POST['sevastatus3']
    status4 = request.POST['sevastatus4']
    status5 = request.POST['sevastatus5']
    status6 = request.POST['sevastatus6']
    status7 = request.POST['sevastatus7']
    status8 = request.POST['sevastatus8']
    status9 = request.POST['sevastatus9']
    status10 = request.POST['sevastatus10']
    status11 = request.POST['sevastatus11']
    status12 = request.POST['sevastatus12']
    status13 = request.POST['sevastatus13']
    status14 = request.POST['sevastatus14']
    status15 = request.POST['sevastatus15']
    id = request.POST['user']

    user_details = get_user_model().objects.get(pk=id)
    statuslist = [status1,status2,status3,status4,status5,status6,status7,status8,
                  status9,status10,status11,status12,status13,status14,status15]
    seva_status = 'inprogress'
    for i in statuslist:
        print('value of i',i)
        if i == 'False':
            seva_status = 'inprogress'
            print('seva_status when false:',seva_status)
            break
        else:
            seva_status = 'completed'
            print('seva_status when true:', seva_status)
    print('final seva_status:', seva_status)

    record = seva_data.objects.get(seva_id=seva_id)
    record.status1 = status1
    record.status2 = status2
    record.status3 = status3
    record.status4 = status4
    record.status5 = status5
    record.status6 = status6
    record.status7 = status7
    record.status8 = status8
    record.status9 = status9
    record.status10 = status10
    record.status11 = status11
    record.status12 = status12
    record.status13 = status13
    record.status14 = status14
    record.status15 = status15
    record.seva_status = seva_status
    record.anubhav = anubhav
    record.save()
    messages.info(request, ' ✅ सेवा अपडेटेड कम्प्लिटेड  ✅ ')
    type = user_details.type
    if type == 'sampark_sevekari':
        return render(request, 'home_sampark_sevekari.html', {'user_details': user_details})
    elif type == 'main_admin':
        return render(request, 'home_admin.html', {'user_details': user_details})
    elif type == 'verified':
        return render(request, 'home_prashankarta.html', {'user_details': user_details})








