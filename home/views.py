from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from common.models import sampark_sevekari
#from django.contrib.auth.models import User
import random
from django.contrib.auth import get_user_model,logout,authenticate

User = get_user_model()

# Create your views here.
code = '1234'
g_email = ''

# function homepage will load home page of the website


def homepage(request):
    return render(request,'homepage.html')


# function annadanpage will load annadanpage page of the website

def annadanpage(request):
    return render(request,'annadan.html')

# function sahityapage will load sahitya page of the website

def sahityapage(request):
    return render(request,'sahitya.html')

# function loginpage will load loginpage of the website

def loginpage(request):
    return render(request,'loginpage.html')

# function registerpage will load registerpage of the website


def registerpage(request):
    return render(request,'registerpage.html')

# function register will load register of the website


def register(request):
    return render(request,'register.html')

# function send_email will send email and verification code on given email address by user

def send_email(request):
    global code, g_email
    g_email = request.POST['email']
    code = str(random.randrange(1000, 9999))
    print(code)
    msg = 'नोंदणीसाठी तुमचा व्हेरीफिकेशन  कोड :'+ code +' हा राहील '
    send_mail('Email Verification', msg, 'samarthview@gmail.com',
              [g_email, 'gurumargdarshan14@gmail.com'], fail_silently=True)

    messages.info(request,
                  '📧 तुमच्या  ई-मेल वर  कोड पाठविण्यात आला आहे , १ मिनिट  थांबा ,\n  कोड नाही आला तर तुम्ही दिलेला ई-मेल बरोबर आहे , ते पहा 📧 ')
    function = 'verify_email'
    return render(request, 'register.html',{'function':function})

# function verify_ecode will verify ecode
def verify_ecode(request):
    global code,g_email
    ecode = request.POST['ecode']
    print('ecode:', ecode)
    print('code:', code)
    if ecode == code:
        data = sampark_sevekari.objects.filter(status='active')
        messages.info(request, ' ✅ ई-मेल व्हेरीफिकेशन  यशस्वी ✅ ')
        function= 'register_form'
        email= g_email
        return render(request, 'register.html',{'function':function,'email':email,'data':data})

    else:
        function = 'verify_email'
        messages.info(request, '❌ ई-मेल कोड चुकीचा आहे ,पुन्हा प्रयत्न करा ❌')
        return render(request, 'register.html',{'function':function})


# function registration_check will verify user details and register the user
def registration_check(request):

    upsarg = request.POST['listname']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    city = request.POST['city']
    code1 = request.POST['mcode']
    mobile1 = request.POST['mobile']
    code2 = request.POST['wmcode']
    mobile2 = request.POST['w_mobile']
    reffered_by = request.POST['reffered_by']
    sscode1 = request.POST['sscode1']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    type = 'unverified'

    datavalue = {'upsarg': upsarg, 'first_name': first_name, 'last_name': last_name, 'city': city, 'mcode': code1,
                 'mobile': mobile1,'email':email,'wmcode': code2, 'w_mobile': mobile2, 'reffered_by': reffered_by, 'sscode': sscode1}

    if password2 == password1:
        if mobile1.isnumeric():
            if len(mobile1) == 10:
                if User.objects.filter(mobile1=mobile1).exists():
                    messages.info(request, 'मोबाइल नंबर रजिस्टर  आहे , कृपया लॉगीन करा ')
                    return render(request, 'loginpage.html')
                else:
                    newuser = User.objects.create_user(upsarg=upsarg, first_name=first_name, last_name=last_name,
                      code1=code1, mobile1=mobile1, code2=code2, mobile2=mobile2,
                      email=email, city=city,
                      reffered_by=reffered_by, type=type, sscode=sscode1,
                       password=password1)
                    newuser.save()
                    messages.info(request, '✅ नोंदणी पूर्ण झाली आहे ✅ ')
                    ss_record = sampark_sevekari.objects.get(sscode=sscode1)
                    print('ss record:', ss_record)
                    ss_id = ss_record.User_id_id
                    ss_details = get_user_model().objects.get(id=ss_id)
                    ss_email = ss_details.email
                    msg = first_name + ' ' + last_name + ' ' + 'यांनी तुमच्या वतीने नोंदणी केली आहे . त्यांना ओळखत असल्यास व्हेरिफाय करा '
                    send_mail('New user registered', msg, 'gurumargdarshan14@gmail.com',
                              [ss_email, 'gurumargdarshan14@gmail.com'], fail_silently=True)

                    return render(request, 'loginpage.html')


            else:
                messages.info(request, '⚠️अपूर्ण मोबाईल नंबर ⚠️')
                function = 'register_form'
                return render(request, 'register.html', {'function': function, 'datavalue': datavalue})
        else:
            messages.info(request, '⚠️ मोबाईल  नंबर  संख्येत अपेक्षित आहे ⚠️')
            function = 'register_form'
            return render(request, 'register.html', {'function': function, 'datavalue': datavalue})
    else:
        messages.info(request, ' ❗ दोन्ही पासवर्ड सारखे पाहिजे ❗')
        function = 'register_form'
        return render(request, 'register.html', {'function': function, 'datavalue': datavalue})

# function applogin will authenticate the user and accordingly login into system


def applogin(request):
    mobile1=request.POST['mobile1']
    password=request.POST['password']
    user = authenticate(username=mobile1,password=password)
    if user is not None:
        user_details = get_user_model().objects.get(mobile1=mobile1)
        type= user_details.type

        if type == 'sampark_sevekari':
            return render(request, 'home_sampark_sevekari.html',{'user_details':user_details})
        elif type == 'main_admin':
            return render(request, 'home_admin.html',{'user_details':user_details})
        elif type == ('unverified') or ('verified'):
         return render(request, 'home_Prashankarta.html',{'user_details':user_details})
    else:
        messages.error(request, 'मोबाईल  किंवा पासवर्ड चुकीचा आहे , पुन्हा लॉगिन करा' )
        return render(request,'loginpage.html')




# function userlogout will log out the user


def userlogout(request):
        logout(request)
        return render(request, 'homepage.html')