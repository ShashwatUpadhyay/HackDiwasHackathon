from django.db import models
from account.models import Student
from course.models import Course
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from hd.email_sender import certified

# Create your models here.
class Certificate(models.Model):
    uid = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    created_at = models.DateField()

    def __str__(self):
        return f"{self.user.full_name} - {self.course.title}"
    

@receiver(post_save, sender=Certificate)
def Certification(sender, instance, created, **kwargs):
    if created:
        email = instance.user.user.email
        print( "email: ",email)
        certified(email,instance)
