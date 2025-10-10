from django.db import models
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from hd.email_sender  import course_purchased
import os
import subprocess
from django.conf import settings
from moviepy import VideoFileClip

# Create your models here.
class CourseCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='course_categories/')
    slug = models.SlugField(unique=True, null=True, blank=True)  
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CourseCategory,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class CourseSubCategory(models.Model):  
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)  
    image = models.ImageField(upload_to='course_subcategories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CourseSubCategory,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    level_choice = (('Beginner','Beginner'),('Intermediate','Intermediate'),('Advance','Advance'))
    teacher = models.ForeignKey('account.Teacher', on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)  
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/')
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    subcategory = models.ForeignKey(CourseSubCategory, on_delete=models.CASCADE, default='Beginner',related_name='courses')
    level = models.CharField(max_length=20, choices=level_choice, null=True, blank=True)
    duration = models.CharField(max_length=30, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course,self).save(*args, **kwargs)
    
    @property
    def latest_vdo_url(self):
        return self.lessons.latest
        
    @property
    def lesson_count(self):
        return len(self.lessons.all())
        
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)  
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    content = models.FileField(upload_to='lessons/')
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 
        super(Lesson,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

@receiver(post_save, sender=Lesson)
def convert_to_hls(sender, instance, **kwargs):
    if instance.content:
        print(instance.content.name)
        input_path = os.path.join(settings.MEDIA_ROOT,instance.content.name)
        output_dir = os.path.join(settings.MEDIA_ROOT, 'videos', str(instance.uid))
        print(input_path, '\n',output_dir)
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'index.m3u8')

        # Skip if already exists (to avoid repeated conversion)
        if os.path.exists(output_path):
            return

        command = [
            'ffmpeg',
            '-i', input_path,
            '-codec:', 'copy',
            '-start_number', '0',
            '-hls_time', '10',
            '-hls_list_size', '0',
            '-f', 'hls',
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print("FFmpeg Error:", e)

    
class Enrollment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    @property
    def progress(self):
        lessons = self.course.lessons.all()
        completed = Progress.objects.filter(student=self.student, lesson__in=lessons).count()
        print(completed, len(lessons))
        return int((completed/len(lessons)*100)) if lessons else 0

@receiver(post_save, sender=Enrollment)
def resultAnounced(sender, instance, created, **kwargs):
    if created:
        course_purchased(instance)


class Progress(models.Model):
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed_at = models.DateTimeField(auto_now_add=True)
    watch_time = models.IntegerField(default=0)  # in seconds
    
    def video_length(self):
        video_path = os.path.join(self.lesson.content.path)
        try:
            clip = VideoFileClip(video_path)
            length = clip.duration
            clip.close()
            return int(length) if length else 0
        except Exception as e:
            print(f"Error reading video duration: {e}")
            return 0


    def __str__(self):
        return f"{self.student} completed {self.lesson}"

# class Comment(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
#     student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='comments')
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.student} commented on {self.lesson}"

# class Rating(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='ratings')
#     student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='ratings')
#     rating = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.student} rated {self.lesson}"
