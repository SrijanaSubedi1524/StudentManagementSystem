from django.shortcuts import render

# Create your views here.
def TeacherDashboard(request):
    return render(request, 'TeacherDashboard/teacher_dashboard.html')