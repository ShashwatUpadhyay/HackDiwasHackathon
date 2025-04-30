from django.shortcuts import render,get_object_or_404
from . import models
# Create your views here.
def courses(request):
    course = models.Course.objects.filter(is_active = True)
    return render(request,'courses.html',{'courses':course})

def category_courses(request, slug):
    cate = get_object_or_404(models.CourseCategory, slug=slug)
    course = models.Course.objects.filter(is_active = True,category=cate)
    return render(request,'courses.html',{'courses':course,'cate':cate})

def subcategory_courses(request, slug, sub):
    cate = get_object_or_404(models.CourseCategory, slug=slug)
    subcate = get_object_or_404(models.CourseSubCategory, slug=sub)
    course = models.Course.objects.filter(is_active = True,subcategory=subcate)
    return render(request,'courses.html',{'courses':course,'cate':cate,'subcate':subcate})