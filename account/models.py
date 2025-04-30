from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from course.models import CourseCategory,CourseSubCategory
import uuid
# Create your models here.
class Student(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    full_name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name
    
class Teacher(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='teachers/', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    adhaar_number = models.CharField(max_length=12, null=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True,blank=True)
    subcategory = models.ForeignKey(CourseSubCategory, on_delete=models.SET_NULL, null=True,blank=True)
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name
    
    @property
    def course_count(self):
        return len(self.courses.all())
    
    @property
    def total_student(self):
        enrollments = 0
        for course in self.courses.all():
            enrollments += len(course.enrollments.all())
        return enrollments