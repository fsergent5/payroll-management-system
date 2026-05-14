"""
URL configuration for COSC641_Payroll_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from payroll import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),

    path('employee/', views.employee_portal, name='employee_portal'),
    path('timesheet/', views.timesheet_portal, name='timesheet_portal'),

    path('employer/', views.employer_dashboard, name='employer_dashboard'),

    path('approve-timesheet/<int:timesheet_id>/', views.approve_timesheet, name='approve_timesheet'),

    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('update-department/<int:department_id>/', views.update_department, name='update_department'),
    path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),

    path('update-position/<int:position_id>/', views.update_position, name='update_position'),
    path('delete-position/<int:position_id>/', views.delete_position, name='delete_position'),
]