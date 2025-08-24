from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    """
    Handle login for students, teachers, and admins
    """
    if request.method == 'POST':
        # Check which form was submitted based on form fields
        if 'student_id' in request.POST:
            student_id = request.POST.get('student_id', '').strip()
            password = request.POST.get('password', '')
            
            if student_id and password:
                user = authenticate(request, username=student_id, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome, {user.first_name or student_id}!')
                else:
                    messages.error(request, 'Invalid student ID or password.')
            else:
                messages.error(request, 'Please fill in all fields.')
                
        elif 'teacher_id' in request.POST:
            teacher_id = request.POST.get('teacher_id', '').strip()
            password = request.POST.get('password', '')
            
            if teacher_id and password:
                user = authenticate(request, username=teacher_id, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, Teacher {user.first_name or teacher_id}!')
                else:
                    messages.error(request, 'Invalid teacher ID or password.')
            else:
                messages.error(request, 'Please fill in all fields.')
                
        elif 'admin_username' in request.POST:
            admin_username = request.POST.get('admin_username', '').strip()
            password = request.POST.get('password', '')
            
            if admin_username and password:
                user = authenticate(request, username=admin_username, password=password)
                if user is not None and user.is_active and (user.is_staff or user.is_superuser):
                    login(request, user)
                    messages.success(request, f'Welcome, Administrator {user.first_name or admin_username}!')
                else:
                    messages.error(request, 'Invalid admin credentials or insufficient permissions.')
            else:
                messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'auth_app/login.html')

def register_view(request):
    """
    Handle user registration
    """
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Basic validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'auth_app/register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth_app/register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'auth_app/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth_app/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth_app/register.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'auth_app/register.html')