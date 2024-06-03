from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=50)
    ageRange = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)