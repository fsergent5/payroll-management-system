from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Employee, Department, Position, Payroll, Timesheet, Attendance
from .forms import DepartmentForm, PositionForm, EmployeeForm, PayrollForm, TimesheetForm, AttendanceForm


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        department_key = request.POST.get("department_key", "").strip()

        user = authenticate(request, username=username, password=password)

        if not user:
            return render(request, 'payroll/login.html', {
                'error': 'Invalid username or password'
            })

        employee = Employee.objects.filter(user=user).first()

        if not employee or not employee.department:
            return render(request, 'payroll/login.html', {
                'error': 'Employee profile not properly set up'
            })

        # Department key check. It is active so the login matches the project requirement.
        if employee.department.department_id.strip().upper() != department_key.strip().upper():
            return render(request, 'payroll/login.html', {
                'error': 'Invalid department key'
            })

        login(request, user)

        if employee.department.department_name.strip().lower() == "admin":
            return redirect('employer_dashboard')

        return redirect('employee_portal')

    return render(request, 'payroll/login.html')


# -------------------------
# EMPLOYEE PORTAL (Employee ONLY)
# -------------------------
@login_required
def employee_portal(request):

    employee = Employee.objects.filter(user=request.user).first()

    if not employee:
        return render(request, 'payroll/employee_portal.html', {
            'error': 'No employee profile linked to this user'
        })

    if request.method == "POST":
        form = TimesheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.employee = employee
            timesheet.approved = False
            timesheet.save()
            return redirect('employee_portal')

    timesheets = Timesheet.objects.filter(employee=employee).order_by('-week_start')
    payroll_records = Payroll.objects.filter(employee=employee).order_by('-pay_period_start')
    attendance_records = Attendance.objects.filter(employee=employee).order_by('-work_date')

    return render(request, 'payroll/employee_portal.html', {
        'employee': employee,
        'payroll_records': payroll_records,
        'timesheets': timesheets,
        'attendance_records': attendance_records,
    })
# -------------------------
# DELETE EMPLOYEE
# -------------------------
@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employer_dashboard')


# -------------------------
# DELETE POSITION
# -------------------------
@login_required
def delete_position(request, id):
    position = get_object_or_404(Position, id=id)
    position.delete()
    return redirect('employer_dashboard')

# -------------------------
# TIMESHEET PORTAL (Employee ONLY)
# -------------------------
@login_required
def timesheet_portal(request):

    employee = Employee.objects.filter(user=request.user).first()
    if not employee:
        return redirect('employee_portal')

    if request.method == "POST":
        form = TimesheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.employee = employee
            timesheet.approved = False
            timesheet.save()
            return redirect('employee_portal')
    else:
        form = TimesheetForm()

    return render(request, 'payroll/timesheet_portal.html', {
        'form': form,
    })


# -------------------------
# EMPLOYER DASHBOARD (ADMIN ONLY)
# -------------------------
@login_required
def employer_dashboard(request):

    employee = Employee.objects.filter(user=request.user).first()

    # restrict access to admin only
    if not employee or not employee.department or employee.department.department_name.lower() != "admin":
        return redirect('employee_portal')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'department':
            form = DepartmentForm(request.POST, prefix='department')
            if form.is_valid():
                form.save()
            return redirect('employer_dashboard')

        elif form_type == 'position':
            form = PositionForm(request.POST, prefix='position')
            if form.is_valid():
                form.save()
            return redirect('employer_dashboard')

        elif form_type == 'employee':
            employee_form = EmployeeForm(request.POST, prefix='employee')

            username = request.POST.get('username')
            password = request.POST.get('password')

            if not employee_form.is_valid():
                return render(request, 'payroll/employer_dashboard.html', {
                    'employee_form': employee_form,
                    'error': employee_form.errors
                })

            if not username or not password:
                return render(request, 'payroll/employer_dashboard.html', {
                    'employee_form': employee_form,
                    'error': 'Missing username or password'
                })

            if User.objects.filter(username=username).exists():
                return render(request, 'payroll/employer_dashboard.html', {
                    'employee_form': employee_form,
                    'error': 'Username already exists'
                })

            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                new_employee = employee_form.save(commit=False)
                new_employee.user = user
                new_employee.save()

            return redirect('employer_dashboard')

        elif form_type == 'timesheet':
            form = TimesheetForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('employer_dashboard')

        elif form_type == 'payroll':
            form = PayrollForm(request.POST, prefix='payroll')
            if form.is_valid():
                form.save()
            return redirect('employer_dashboard')

    return render(request, 'payroll/employer_dashboard.html', {
        'department_form': DepartmentForm(prefix='department'),
        'position_form': PositionForm(prefix='position'),
        'employee_form': EmployeeForm(prefix='employee'),
        'timesheet_form': TimesheetForm(),
        'payroll_form': PayrollForm(prefix='payroll'),
        'attendance_form': AttendanceForm(),

        # admin sees ALL
        'employees': Employee.objects.select_related('department', 'position').all(),
        'departments': Department.objects.all(),
        'positions': Position.objects.all(),
        'attendance_records': Attendance.objects.select_related('employee').all(),
        'timesheet_records': Timesheet.objects.select_related('employee', 'employee__position').order_by('-week_start'),
        'payroll_records': Payroll.objects.select_related('employee').order_by('-pay_period_start'),
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'active_employees': Employee.objects.filter(status='ACTIVE').count(),
    })


# -------------------------
# APPROVE TIMESHEET AND CREATE PAYROLL
# -------------------------
@login_required
def approve_timesheet(request, timesheet_id):
    admin_employee = Employee.objects.filter(user=request.user).first()

    if not admin_employee or not admin_employee.department or admin_employee.department.department_name.lower() != "admin":
        return redirect('employee_portal')

    timesheet = get_object_or_404(Timesheet, id=timesheet_id)

    total_hours = timesheet.total_hours()
    regular_hours = min(total_hours, Decimal('40.00'))
    overtime_hours = max(total_hours - Decimal('40.00'), Decimal('0.00'))

    # Annual salary is converted to an hourly rate using 2,080 work hours per year.
    hourly_rate = timesheet.employee.position.base_salary / Decimal('2080.00')

    base_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * hourly_rate * Decimal('1.50')
    gross_salary = base_pay + overtime_pay

    tax_deduction = gross_salary * Decimal('0.12')
    insurance_deduction = Decimal('50.00')
    net_salary = gross_salary - tax_deduction - insurance_deduction

    Payroll.objects.update_or_create(
        employee=timesheet.employee,
        pay_period_start=timesheet.week_start,
        pay_period_end=timesheet.week_end,
        defaults={
            'base_pay': base_pay,
            'overtime_pay': overtime_pay,
            'gross_salary': gross_salary,
            'tax_deduction': tax_deduction,
            'insurance_deduction': insurance_deduction,
            'net_salary': net_salary,
        }
    )

    timesheet.approved = True
    timesheet.save()

    return redirect('employer_dashboard')
