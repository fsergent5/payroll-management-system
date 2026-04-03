# Payroll Management System

## Project Overview
This project is a web-based payroll management system designed to manage employee records, attendance tracking, salary calculations, and payroll processing for a company. The system allows employers to efficiently store and manage data related to departments, job positions, employees, attendance, and payroll records.

The application is built using Django for the backend and Python for server-side logic, with a relational database structure that enforces data integrity through primary and foreign key relationships.

---

## Features
- Create and manage departments  
- Define job positions with base salaries  
- Register and manage employees  
- Track employee attendance and overtime hours  
- Generate and store payroll records  
- View employee, attendance, and payroll data in a structured dashboard  

---

## Technologies Used
- Python  
- Django (Backend Framework)  
- SQLite (Database)  
- HTML/CSS (Frontend)  
- Git & GitHub (Version Control)  

---

## Database Design
The system is based on a relational database model with the following entities:

- Department  
- Position  
- Employee  
- Attendance  
- Payroll  

Relationships are enforced using foreign keys to ensure referential integrity and consistency across the system.

---

## Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/payroll-management-system.git
2. Navigate into the project folder:
cd payroll-management-system
3. Install dependencies:
pip install django
4. Apply migrations:
python manage.py migrate
5. Run the server:
python manage.py runserver
6. Open in browser:
http://127.0.0.1:8000/

Usage
Use the Employer Dashboard to add and manage:
Departments
Positions
Employees
Attendance records
Payroll data
View stored records in tables directly on the dashboard
