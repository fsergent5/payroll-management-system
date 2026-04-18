# employees/urls.py

from django.urls import path
from . import views
from django.shortcuts import render

#urlpatterns = [
#  path('', views.employee_portal, name='employee_portal'),
#  path('timesheet/', views.timesheet_portal, name='timesheet_portal'),
#]



def employer_dashboard(request):
    return render(request, 'employer_dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def timesheet_portal(request):
    return render(request, 'navigation/timesheet_portal.html')