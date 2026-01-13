from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Products(models.Model):
    pname = models.CharField(max_length=100)
    pdesc = models.CharField(max_length=200)
    price = models.IntegerField()
    pcategory =models.CharField(max_length=100)
    trending = models.BooleanField(default=False)
    offer=models.BooleanField(default=False)
    pimages=models.ImageField(default='rose.jpeg',upload_to='uploads')

class CartModel(models.Model):
    pname=models.CharField(max_length=100)
    price=models.IntegerField()
    pcategory=models.CharField(max_length=100)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    host=models.ForeignKey(User,on_delete=models.CASCADE)