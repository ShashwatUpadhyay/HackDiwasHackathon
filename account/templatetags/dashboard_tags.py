
from django import template
from django.shortcuts import get_object_or_404
from course.models import Course, Enrollment, Progress
from account.models import Student
register = template.Library()


@register.filter
def lesson_count(user):
    enrollments = user.enrollments.all()
    total_lessons = 0
    for enrollment in enrollments:
        total_lessons += enrollment.course.lessons.count()
    return total_lessons

@register.filter
def progress(course,user):
    lessons = course.lessons.all()
    completed = Progress.objects.filter(lesson__in=lessons,student=user).count()
    return int((completed/lessons.count())*100) if lessons.count() > 0 else 0
    
