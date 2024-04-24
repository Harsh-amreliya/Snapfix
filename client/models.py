from django.db import models
from adminh.models import User
from stores.models import productlisting
from servicestore.models import servicelisting

# Create your models here.

class UserLocation(models.Model):
    latitude=models.FloatField()
    longitude=models.FloatField()

class liststorerequest(models.Model):
    listed=models.BooleanField(default=False,blank=True,null=True)
    username=models.CharField(max_length=40)
    storename=models.CharField(max_length=60)
    email=models.EmailField(max_length=60)
    type=models.CharField(max_length=30)

class mycart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    productid=models.ForeignKey(productlisting,on_delete=models.CASCADE,blank=True,null=True)
    serviceid=models.ForeignKey(servicelisting,on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.IntegerField(default=1)


class towingrequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=60)
    clientlocation=models.CharField(max_length=150)
    additionalprobleminfo=models.CharField(max_length=100,blank=True,null=True)
    contact=models.BigIntegerField()
    storeid=models.IntegerField(blank=True,null=True)
    serviceid=models.CharField(max_length=80)
    totalprice=models.BigIntegerField()
    date=models.DateTimeField(auto_now_add=True)
    istowable=models.BooleanField(blank=True,null=True,default=0)
    completed=models.BooleanField(blank=True,null=True,default=0)

class productrequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=60)
    address=models.CharField(max_length=150)
    contact=models.BigIntegerField()
    productid=models.CharField(max_length=80)
    totalprice=models.BigIntegerField()
    date=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(blank=True,null=True,default=0)





