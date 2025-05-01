from django.db import models
from account.models import Student
from course.models import Course
import uuid
# Create your models here.
class Certificate(models.Model):
    uid = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    created_at = models.DateField()

    def __str__(self):
        return f"{self.user.full_name} - {self.course.title}"