from django.db import models

# Create your models here.

class Teacher(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254) 

    phone = models.CharField(max_length=15)

    institute = models.CharField(max_length=254)
    purpose = models.CharField(max_length=254)

    session_token = models.CharField(max_length=10, default=0)

    last_login = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.fullname
    