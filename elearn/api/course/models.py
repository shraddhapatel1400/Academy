from django.db import models
from api.teacher.models import Teacher
import datetime
# Create your models here.

today = datetime.datetime.today()

class Course(models.Model):
    coursename = models.CharField(unique=True,max_length=100)
    description = models.CharField(max_length=254) 

    image = models.ImageField(upload_to='images/course/')

    price = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,blank=True, null=True)
    popular = models.BooleanField(blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coursename
    