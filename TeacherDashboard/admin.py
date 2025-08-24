from django.contrib import admin

# Register your models here.

from .models import Teacher, Student, Course, StudentCourse, Attendance, Leave

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(StudentCourse)
admin.site.register(Attendance)
admin.site.register(Leave)
