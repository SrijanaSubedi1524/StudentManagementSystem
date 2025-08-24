from django.urls import path
from TeacherDashboard import views

urlpatterns = [
    path('dashboard/', views.TeacherDashboard, name='teacher_dashboard')
]