from django.contrib import admin
from .models import Department, Position, Employee, Attendance, Payroll

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Payroll)
