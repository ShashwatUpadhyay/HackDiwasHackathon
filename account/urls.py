from django.urls import path
from . import views
urlpatterns = [
    path('verify/<uid>/', views.verify, name='verify'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/<uid>/', views.teacher_profile, name='teacher_profile'),
    path('add-course/', views.add_course, name='add_course'),
    path('my-course/', views.teacher_my_course, name='teacher_my_course'),
    path('teacher-go-live/', views.teacher_go_live, name='teacher_go_live'),
    path('my-course-enrollments/<uid>/', views.teacher_my_course_students, name='teacher_my_course_students'),
    
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    
]