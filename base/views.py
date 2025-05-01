from django.shortcuts import render, HttpResponse
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
    course = Course.objects.filter(is_active = True)
    teacher = Teacher.objects.all()
    return render(request,'student-explore.html',{'courses':course,'teachers':teacher})

def exploreTeacher(request):
    return render(request,'teacher-explore.html')

