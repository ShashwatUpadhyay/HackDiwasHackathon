from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from course.models import Course, CourseCategory, CourseSubCategory

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
        email= str(request.POST.get('email'))
        password= request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        role = request.POST.get('role')
        
        if User.objects.filter(email=email.lower()).exists():
            return render(request, 'auth/register.html', {'error': 'Email already exists'})
        
        if password != confirm_password:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=email, email=email.lower())
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

@login_required(login_url='login')
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher_dashboard.html')

@login_required(login_url='login')
def add_course(request):
    cate = CourseCategory.objects.all()
    subcate = CourseSubCategory.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        subcategory = request.POST.get('type')
        price = request.POST.get('price')
        print(title, description, image, category, subcategory)
        if Course.objects.filter(title=title).exists():
            messages.error(request, 'Course with this title already exists')
            return redirect('add_course')
        course = Course.objects.create(
            teacher=request.user.teacher,
            title=title,
            description=description,
            image=image,
            category=CourseCategory.objects.get(slug=category),
            subcategory=CourseSubCategory.objects.get(slug=subcategory),
        )
        if price:
            course.price = price
        else:
            course.is_free = True
        
        course.save()
        messages.success(request, 'Course created successfully')
        return redirect('teacher_dashboard')

    context = {
        'categories': cate,
        'subcategories': subcate,
    }
    return render(request, 'dashboard/teacher_add_course.html',context)

@login_required(login_url='login')
def teacher_my_course(request):
    courses = Course.objects.filter(teacher__user=request.user)
    context = {
        'courses': courses,
    }
    return render(request, 'dashboard/teacher_my_course.html', context)