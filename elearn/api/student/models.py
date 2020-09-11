from django.db import models
from api.course.models import Course
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Student(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254) 
    image = models.ImageField(upload_to='images/student/',blank=True, null=True)
    phone = models.CharField(max_length=15,blank=True, null=True)

    session_token = models.CharField(max_length=10, default=0)

    last_login = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.fullname
    