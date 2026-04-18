from django.shortcuts import render, redirect
from .models import Employee, Department, Position, Attendance,Payroll
from .forms import DepartmentForm, PositionForm, EmployeeForm, AttendanceForm, PayrollForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        department_key = request.POST.get("department_key")

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

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # ---------------- Attendance (Employee ONLY)
        if form_type == 'attendance':
            form = AttendanceForm(request.POST, prefix='attendance')
            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.employee = employee
                attendance.save()
            return redirect('employee_portal')

    attendance_records = Attendance.objects.filter(employee=employee)
    payroll_records = Payroll.objects.filter(employee=employee)

    return render(request, 'payroll/employee_portal.html', {
        'employee': employee,
        'attendance_records': attendance_records,
        'payroll_records': payroll_records,
    })


# -------------------------
# TIMESHEET PORTAL (Employee ONLY)
# -------------------------
@login_required
def timesheet_portal(request):

    employee = Employee.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.employee = employee
            attendance.save()
            return redirect('employee_portal')

    return render(request, 'payroll/timesheet_portal.html', {
        'form': AttendanceForm(),
      
    })


# -------------------------
# EMPLOYER DASHBOARD (ADMIN ONLY)
# -------------------------
@login_required
def employer_dashboard(request):

    employee = Employee.objects.filter(user=request.user).first()

    #  restrict access to admin only
    if not employee or employee.department.department_name.lower() != "admin":
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

                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()

            return redirect('employer_dashboard')

        elif form_type == 'attendance':
            form = AttendanceForm(request.POST, prefix='attendance')
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
        'attendance_form': AttendanceForm(prefix='attendance'),
        'payroll_form': PayrollForm(prefix='payroll'),

        # admin sees ALL
        'employees': Employee.objects.select_related('department', 'position').all(),
        'departments': Department.objects.all(),
        'positions': Position.objects.all(),
        'attendance_records': Attendance.objects.select_related('employee').all(),
        'payroll_records': Payroll.objects.select_related('employee').all(),
    })