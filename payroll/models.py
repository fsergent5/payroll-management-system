from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_id= models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.department_name
    


class Position(models.Model):
    position_title = models.CharField(max_length=100)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.position_title


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    hire_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.work_date}"


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    base_pay = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee} Payroll ({self.pay_period_start} to {self.pay_period_end})"
    
class Timesheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    week_start = models.DateField()
    week_end = models.DateField()

    mon_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tues_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    wed_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    thurs_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fri_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sat_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sun_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)