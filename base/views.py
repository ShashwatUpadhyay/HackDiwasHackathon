from django.shortcuts import render, HttpResponse
from django.db.models import Q
from course.models import CourseCategory, Course
from account.models import Teacher
# Create your views here.
def home(request):
    cate = CourseCategory.objects.all()
    context = {
        'cate': cate,
    }
    return render(request,'home.html',context)

def explore(request):
    courses = Course.objects.filter(is_active=True)
    teachers = Teacher.objects.all()
    
    # Handle search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Search in course titles, descriptions, and teacher names
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(teacher__full_name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(subcategory__name__icontains=search_query)
        )
        
        # Also search teachers
        teachers = teachers.filter(
            Q(full_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(subcategory__name__icontains=search_query)
        )
    
    context = {
        'courses': courses,
        'teachers': teachers,
        'search_query': search_query,
    }
    return render(request, 'student-explore.html', context)

def exploreTeacher(request):
    return render(request,'teacher-explore.html')

