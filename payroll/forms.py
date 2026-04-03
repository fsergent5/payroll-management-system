from django import forms
from .models import Department, Position, Employee, Attendance, Payroll


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position_title', 'base_salary']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'department', 'position', 'hire_date', 'status']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'})
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'work_date', 'hours_worked', 'overtime_hours']
        widgets = {
            'work_date': forms.DateInput(attrs={'type': 'date'})
        }


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee',
            'pay_period_start',
            'pay_period_end',
            'base_pay',
            'overtime_pay',
            'gross_salary',
            'tax_deduction',
            'insurance_deduction',
            'net_salary'
        ]
        widgets = {
            'pay_period_start': forms.DateInput(attrs={'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'type': 'date'}),
        }