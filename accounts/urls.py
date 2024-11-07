
from django.urls import path
from .import views

urlpatterns = [
    
    path('',views.homepage),
    path('login/',views.Login),
    path('register/',views.Register),
    path('secure/<uid>',views.SecureAppointment),
    path('make-appointment/<did>/<uid>',views.makeappoint),
    path('logout/',views.Logout),
    path('news/',views.news),
   
]
