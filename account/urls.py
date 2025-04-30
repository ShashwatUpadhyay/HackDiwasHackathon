from django.urls import path
from . import views
urlpatterns = [
    path('verify/<uid>/', views.verify, name='verify'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('my-course/', views.teacher_my_course, name='teacher_my_course'),
]