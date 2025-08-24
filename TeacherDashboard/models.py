from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # Link to Django's User model for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Basic Information
    teacher_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(help_text="YYYY-MM-DD", verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    
    # Professional Information
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    CLASS_CHOICES = [
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]
    
    # Link to Django's User model for authentication (optional for students)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Basic Information
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(help_text="YYYY-MM-DD", verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Academic Information
    current_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Course is taught by a teacher
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    
    # Which class this course is for
    class_level = models.CharField(max_length=2, choices=Student.CLASS_CHOICES)
    
    # Academic session/year
    academic_year = models.CharField(max_length=9, default='2024-2025')  # Format: YYYY-YYYY
    semester = models.CharField(max_length=20, default='First Semester')
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['class_level', 'course_name']
        unique_together = ['course_code', 'academic_year']
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class StudentCourse(models.Model):
    """Junction table for many-to-many relationship between Student and Course with marks"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Marks and grades
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade = models.CharField(max_length=2, blank=True)  # A+, A, B+, etc.
    
    # Enrollment details
    is_completed = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['course__course_name']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_name}"
    
    @property
    def percentage(self):
        if self.marks_obtained and self.total_marks:
            return (self.marks_obtained / self.total_marks) * 100
        return 0
    
    def calculate_grade(self):
        """Auto-calculate grade based on percentage"""
        percentage = self.percentage
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'


class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),    
    ]
    
    # Generic fields for both teachers and students
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=ATTENDANCE_CHOICES)
    remarks = models.TextField(blank=True)
    
    # For students
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='attendances')
    
    # For teachers
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='attendances')
    
    # Additional fields
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ensure one attendance record per person per day
        constraints = [
            models.CheckConstraint(
                check=models.Q(student__isnull=False) | models.Q(teacher__isnull=False),
                name='attendance_must_have_student_or_teacher'
            ),
            models.CheckConstraint(
                check=~(models.Q(student__isnull=False) & models.Q(teacher__isnull=False)),
                name='attendance_cannot_have_both_student_and_teacher'
            ),
        ]
        ordering = ['-date']
    
    def __str__(self):
        person = self.student or self.teacher
        return f"{person.full_name} - {self.date} - {self.get_status_display()}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.student and not self.teacher:
            raise ValidationError("Attendance must be for either a student or teacher")
        if self.student and self.teacher:
            raise ValidationError("Attendance cannot be for both student and teacher")


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
        ('AL', 'Annual Leave'),
        ('ML', 'Medical Leave'),
        ('EL', 'Emergency Leave'),
        ('OT', 'Other'),
    ]
    
    LEAVE_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    
    # For students
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='leaves')
    
    # For teachers
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='leaves')
    
    # Leave details
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=1, choices=LEAVE_STATUS_CHOICES, default='P')
    
    # Approval details
    approved_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_remarks = models.TextField(blank=True)
    
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(student__isnull=False) | models.Q(teacher__isnull=False),
                name='leave_must_have_student_or_teacher'
            ),
            models.CheckConstraint(
                check=~(models.Q(student__isnull=False) & models.Q(teacher__isnull=False)),
                name='leave_cannot_have_both_student_and_teacher'
            ),
        ]
    
    def __str__(self):
        person = self.student or self.teacher
        return f"{person.full_name} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.student and not self.teacher:
            raise ValidationError("Leave must be for either a student or teacher")
        if self.student and self.teacher:
            raise ValidationError("Leave cannot be for both student and teacher")
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date")