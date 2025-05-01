
from django import template
from django.shortcuts import get_object_or_404
from course.models import Course, Enrollment, Progress
from account.models import Student
register = template.Library()


@register.filter
def enrolled(course,user):
    if hasattr(user, 'student'):
        return Enrollment.objects.filter(course=course, student=user.student).exists()
    else:
        return False
    
@register.filter
def completed(lesson,student):
    return Progress.objects.filter(lesson=lesson,student=student).exists()

@register.filter
def progress(course,student):
    lessons = len(course.lessons.all())
    completed = Progress.objects.filter(lesson__course=course, student=student).count()
    progess = (completed / lessons) * 100 if lessons > 0 else 0
    return int(progess)