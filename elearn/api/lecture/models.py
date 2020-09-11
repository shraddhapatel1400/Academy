from django.db import models
from api.course.models import Course

# Create your models here.
class Lecture(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,blank=True, null=True)
    video = models.FileField(upload_to='video/course',blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title