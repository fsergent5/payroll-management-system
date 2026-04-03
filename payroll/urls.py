from django.urls import path
from .views import employer_dashboard

urlpatterns = [
    path('', employer_dashboard, name='dashboard'),
]