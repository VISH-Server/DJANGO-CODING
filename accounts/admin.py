from django.contrib import admin

from accounts.models import doctor,schedule,userRec,appointment

class doctorRecord(admin.ModelAdmin):
    list_display=('did','dname','dmobile','dqualification','dspecialization','yoe')


class docSchedule(admin.ModelAdmin):
    list_display=('sid','day','time','doctor')

class Rec(admin.ModelAdmin):
    list_display=['mobile','pat']
 
class appoint1(admin.ModelAdmin):
    list_display=['apid','doctor','patient','apmade','apdate']

admin.site.register(appointment,appoint1)
admin.site.register(doctor,doctorRecord)
admin.site.register(schedule,docSchedule)
admin.site.register(userRec,Rec)
# Register your models here.
