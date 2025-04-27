from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        
        if not User.objects.filter(username=email).exists():
            messages.error(request, 'Email does not exist')
            return redirect('login')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            elif hasattr(user, 'student'):
                return redirect('home')
            elif hasattr(user, 'teacher'):
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        elif hasattr(request.user, 'student'):
            return redirect('home')
        elif hasattr(request.user, 'teacher'):
            return redirect('home')
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email= request.POST.get('email')
        password= request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        role = request.POST.get('role')
        
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {'error': 'Email already exists'})
        
        if password != confirm_password:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.save()
        
        if role == 'student':
            models.Student.objects.create(user=user, full_name=full_name)
        elif role == 'teacher': 
            models.Teacher.objects.create(user=user, full_name=full_name)   
            
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'auth/register.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')