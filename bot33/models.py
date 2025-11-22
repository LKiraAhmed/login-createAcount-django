from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=155)