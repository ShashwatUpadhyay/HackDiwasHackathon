from django.shortcuts import render, HttpResponse
from course.models import CourseCategory
# Create your views here.
def home(request):
    cate = CourseCategory.objects.all()
    context = {
        'cate': cate,
    }
    return render(request,'home.html',context)

def explore(request):
    return render(request,'student-explore.html')

def exploreTeacher(request):
    return render(request,'teacher-explore.html')

