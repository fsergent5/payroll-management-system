from django.shortcuts import render, redirect
from .models import Employee, Department, Position, Attendance, Payroll
from .forms import DepartmentForm, PositionForm, EmployeeForm, AttendanceForm, PayrollForm


def employer_dashboard(request):
    department_form = DepartmentForm(prefix='department')
    position_form = PositionForm(prefix='position')
    employee_form = EmployeeForm(prefix='employee')
    attendance_form = AttendanceForm(prefix='attendance')
    payroll_form = PayrollForm(prefix='payroll')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'department':
            department_form = DepartmentForm(request.POST, prefix='department')
            if department_form.is_valid():
                department_form.save()
                return redirect('dashboard')

        elif form_type == 'position':
            position_form = PositionForm(request.POST, prefix='position')
            if position_form.is_valid():
                position_form.save()
                return redirect('dashboard')

        elif form_type == 'employee':
            employee_form = EmployeeForm(request.POST, prefix='employee')
            if employee_form.is_valid():
                employee_form.save()
                return redirect('dashboard')

        elif form_type == 'attendance':
            attendance_form = AttendanceForm(request.POST, prefix='attendance')
            if attendance_form.is_valid():
                attendance_form.save()
                return redirect('dashboard')

        elif form_type == 'payroll':
            payroll_form = PayrollForm(request.POST, prefix='payroll')
            if payroll_form.is_valid():
                payroll_form.save()
                return redirect('dashboard')

    context = {
        'department_form': department_form,
        'position_form': position_form,
        'employee_form': employee_form,
        'attendance_form': attendance_form,
        'payroll_form': payroll_form,
        'employees': Employee.objects.select_related('department', 'position').all(),
        'departments': Department.objects.all(),
        'positions': Position.objects.all(),
        'attendance_records': Attendance.objects.select_related('employee').all(),
        'payroll_records': Payroll.objects.select_related('employee').all(),
    }

    return render(request, 'payroll/employer_dashboard.html', context)
