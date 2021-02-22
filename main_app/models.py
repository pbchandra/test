from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class encrypted_data(models.Model):
    sendby=models.CharField(max_length=30,default='none')
    sendto=models.CharField(max_length=30,default='none')
    nrmlimg = models.ImageField(upload_to ='pics')
    msg = models.TextField()
    sensitivity=models.TextField()
    secret_key=models.TextField()
    encryimg=models.ImageField(upload_to ='pics')
