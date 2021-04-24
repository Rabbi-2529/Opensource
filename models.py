from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Post(models.Model):
    title =models.CharField(max_length=200)
    desc = models.TextField(max_length=20000)
    image=models.ImageField(upload_to="static/osj/images/",default="")
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    messages=models.CharField(max_length=1000)
   






 
    


    



  