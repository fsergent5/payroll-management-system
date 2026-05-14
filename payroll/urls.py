# employees/urls.py

from django.urls import path
from . import views
from django.shortcuts import render

    urlpatterns = [
    path('', views.employee_portal, name='employee_portal'),
    path('timesheet/', views.timesheet_portal, name='timesheet_portal'),
]


