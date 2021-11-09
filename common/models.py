from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from datetime import date


# Create your models here.

class User(AbstractUser):
    username = None
    upsarg = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    code1 = models.CharField(max_length=15, null=True)
    mobile1 = models.CharField(unique=True, max_length=15)
    code2 = models.CharField(max_length=15, null=True)
    mobile2 = models.CharField(max_length=15, null=True)
    reffered_by = models.CharField(max_length=60, null=True)
    type = models.CharField(max_length=30)
    sscode = models.CharField(max_length=5)

    objects = UserManager()

    USERNAME_FIELD = 'mobile1'
    REQUIRED_FIELDS = []

class sampark_sevekari(models.Model):
    objects = None
    sscode = models.CharField(max_length=5)
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,default='active')

class session_data(models.Model):
    objects = None
    session_id = models.AutoField(primary_key=True)
    User_id = models.ForeignKey(User, on_delete= models.CASCADE)
    prashan1 = models.CharField(max_length=200)
    prashan2 = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=30,default='submitted')
    Date_filled = models.CharField(max_length=150,default=str(date.today()))
    schedule_date = models.DateField(null=True)
    schedule_time = models.CharField(max_length=15, null=True)


class st_data(models.Model):
    objects = None
    st_id = models.AutoField(primary_key=True)
    st_date = models.DateField(null=True)
    st_status = models.CharField(max_length=15, null=True)
    st_comment = models.CharField(max_length=50,null=True)

0
class seva_data(models.Model):
    objects = None
    seva_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.ForeignKey(session_data, on_delete=models.CASCADE)
    date_qa = models.DateField(auto_now=True)
    seva1 = models.CharField(max_length=150, default=None)
    seva2 = models.CharField(max_length=150, default=None)
    seva3 = models.CharField(max_length=150, default=None)
    seva4 = models.CharField(max_length=150, default=None)
    seva5 = models.CharField(max_length=150, default=None)
    seva6 = models.CharField(max_length=150, default=None)
    seva7 = models.CharField(max_length=150, default=None)
    seva8 = models.CharField(max_length=150, default=None)
    seva9 = models.CharField(max_length=150, default=None)
    seva10 = models.CharField(max_length=150, default=None)
    seva11 = models.CharField(max_length=150, default=None)
    seva12 = models.CharField(max_length=150, default=None)
    seva13 = models.CharField(max_length=150, default=None)
    seva14 = models.CharField(max_length=150, default=None)
    seva15 = models.CharField(max_length=500, default=None)
    status1 = models.BooleanField(default=False)
    status2 = models.BooleanField(default=False)
    status3 = models.BooleanField(default=False)
    status4 = models.BooleanField(default=False)
    status5 = models.BooleanField(default=False)
    status6 = models.BooleanField(default=False)
    status7 = models.BooleanField(default=False)
    status8 = models.BooleanField(default=False)
    status9 = models.BooleanField(default=False)
    status10 = models.BooleanField(default=False)
    status11 = models.BooleanField(default=False)
    status12 = models.BooleanField(default=False)
    status13 = models.BooleanField(default=False)
    status14 = models.BooleanField(default=False)
    status15 = models.BooleanField(default=False)
    seva_status = models.CharField(max_length=15,  default='inprogress')
    anubhav = models.BooleanField(default=False)
    sahitya = models.BooleanField(default=False)
    seva_explained = models.BooleanField(default=False)
    guru_ans_p1 = models.CharField(max_length=15, default=None)
    guru_ans_p2 = models.CharField(max_length=15,default=None)



