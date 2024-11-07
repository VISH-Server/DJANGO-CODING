

from http.client import HTTPResponse

from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from accounts.models import userRec,schedule,doctor,appointment

import datetime
# Create your views here.
def homepage(request):
    return render(request,'index.html')

def news(request):
    return render(request,'news.html')


def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/secure/{}'.format(username))
        else:
            messages.error(request,"Credentials not found",extra_tags="danger")
            return redirect('/login/')
    else:
        return render(request,'login.html')



def Logout(request):
    logout(request)
    return redirect('/login/')

def makeappoint(request,did,uid):
    if request.user.is_authenticated:
        if request.method=='POST':
            dat=request.POST['dat']
            #dt=dat[:4]+dat[5:7]+dat[8:]
            #dt1=datetime.date.today().strftime('%Y%m%d')
            dt=datetime.datetime.strptime(dat,"%Y-%m-%d").date()
            dt1=datetime.date.today()
            print(dt)
            print(dt1)
            if dt<dt1:
                messages.error(request,"Date must be greater than today")
                return redirect('/make-appointment/{}/{}'.format(did,uid))
            elif (dt-dt1)>datetime.timedelta(days=30):
                messages.error(request,"Date must be within 30 days from today")
                return redirect('/make-appointment/{}/{}'.format(did,uid))
            else:
                wday=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
                ddt=wday[dt.weekday()]
                data=schedule.objects.get(doctor=did)
            
                dtt=(data.day).split(',')
                if ddt in dtt:
                    doc=doctor.objects.get(did=did)
                    u=User.objects.get(username=uid)
                    con=appointment(doctor=doc,patient=u,apdate=dt)
                    con.save()
                    if con is not None:
                        messages.success(request,"Appointment Made Successfully")
                        return redirect('/make-appointment/{}/{}'.format(did,uid))
                    else:
                        messages.error(request,"Appointment Unsuccessful")
                        return redirect('/make-appointment/{}/{}'.format(did,uid))
                else:
                    messages.error(request,"Appointment day wrong")
                    return redirect('/make-appointment/{}/{}'.format(did,uid))

        else:
            data=schedule.objects.raw('SELECT accounts_schedule.*,accounts_doctor.* from accounts_schedule,accounts_doctor where accounts_schedule.doctor_id=accounts_doctor.did and accounts_schedule.doctor_id=%s',did)
            return render(request,"makeappointment.html",{'data':data})
    else:
        return redirect('/login/')


def SecureAppointment(request,uid):
    if request.user.is_authenticated:
        
        u=User.objects.get(username=uid)
        data=schedule.objects.raw('SELECT accounts_schedule.*,accounts_doctor.* from accounts_schedule,accounts_doctor where accounts_schedule.doctor_id=accounts_doctor.did')
        data1=appointment.objects.raw('select a.*,d.*,s.* from accounts_appointment a,accounts_doctor d,accounts_schedule s where a.doctor_id=d.did and s.doctor_id=d.did and a.patient_id={}'.format(u.id))
        
        return render(request,'secure.html',{'data':data,'data1':data1})
    else:
        return redirect('/login/')



def Register(request):  
    

        if request.method=='POST':
           
            fname=request.POST['fname']
            lname=request.POST['lname']
            username=request.POST['username']
            mobile=request.POST['mobile']
            email=request.POST['email']
            password=request.POST['pass1']
            pass2=request.POST['pass2']
            if username=='':
                messages.error(request,"Username must be given")
                return redirect('/register/')
            if mobile=='':
                messages.error(request,"Mobile number must be given")
                return redirect('/register/')
            if email=='':
                messages.error(request,"Email must be given")
                return redirect('/register/')
            if password=='' or pass2=='':
                messages.error(request,"Enter password and confirm")
                return redirect('/register/')
            if password==pass2:
                if User.objects.filter(username=username).exists():
                    messages.error(request,"Username already taken")
                    return redirect('/register/')
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email already taken")
                    return redirect('/register/')
                else:
                        user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
                        
                        user.save()
                       
                        if user is not None:
                            en=userRec(pat=user,mobile=mobile)
                            en.save()
                            messages.success(request,"Registered successfully",extra_tags='success')
                            return redirect('/login/')
                           

            else:
                messages.error(request,"Both passwords are not matching")
               

        else:
            return render(request,'register.html')
