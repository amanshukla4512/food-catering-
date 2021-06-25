from django.db import models
from django.contrib.auth.models import User 

class UserData(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    bio = models.TextField(max_length=500, blank=True) 
    gender = models.CharField(max_length=30) 
    dob = models.DateField() 
    location=models.CharField(max_length=30)
    order=models.TextField(max_length=500)
    tamt=models.IntegerField()

class Menu(models.Model):
	name=models.CharField(max_length=30)
	price=models.IntegerField()
	
 

# Create your models here.
