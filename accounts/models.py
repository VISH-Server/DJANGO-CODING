
from email.policy import default

from django.contrib.auth.models import User
from tabnanny import verbose
from django.db import models


class doctor(models.Model):
    did=models.AutoField(primary_key=True)
    dname=models.CharField(max_length=50,verbose_name='Doctor Name')
    dmobile=models.CharField(max_length=12,verbose_name='Doctor Mobile No.')
    dqualification=models.CharField(max_length=50,verbose_name='Doctor Qualification')
    dspecialization=models.CharField(max_length=50,verbose_name='Doctor Specialization')
    yoe=models.CharField(max_length=50,verbose_name='Doctor Experience')
    
class userRec(models.Model):
    mobile=models.CharField(max_length=12,verbose_name='Patient Mobile No.',blank=False)
    pat=models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient',verbose_name='Patient')
   
    
class schedule(models.Model):
    sid=models.AutoField(primary_key=True)
    day=models.CharField(max_length=50,verbose_name="Doctor's days")
    time=models.CharField(max_length=50,verbose_name='Timing')
    doctor=models.ForeignKey(doctor,on_delete=models.CASCADE,related_name='doctor',verbose_name='Doctor')

class appointment(models.Model):
    apid=models.AutoField(primary_key=True)
    doctor=models.ForeignKey(doctor,on_delete=models.CASCADE,verbose_name='Doctor')
    patient=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Patient')
    apmade=models.DateField(auto_now_add=True,blank=False,verbose_name='Appointment Making Time')
    apdate=models.DateField(verbose_name='Appontment Date')
