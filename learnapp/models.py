from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

user_type = [
    ("VENDOR","Vendor"),
    ("NORMAL_USER","normal_user")
]

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional fields
    phone = models.CharField(max_length=10,unique=True)
    address = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    user_type = models.CharField(max_length=100,choices=user_type,default="NORMAL_USER")