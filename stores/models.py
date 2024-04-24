
from django.db import models

from adminh.models import User


# Create your models here.

class storedata(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   entered_store_details=models.BooleanField(default=False)
   ownername=models.CharField(max_length=70,null=True,blank=True)
   storename=models.CharField(max_length=80 ,null=True,blank=True)
   storecontact=models.BigIntegerField(null=True,blank=True)
   email=models.EmailField(max_length=80,null=True,blank=True)
   openingtime=models.TimeField(null=True,blank=True)
   closingtime=models.TimeField(null=True,blank=True)
   ownercontact=models.BigIntegerField(null=True,blank=True)
   storeaddress=models.CharField(max_length=180,null=True,blank=True)
   storelicencedocument=models.FileField(upload_to='storedata/licence_doc/', blank=True, null=True)
   ownersdocument=models.FileField(upload_to='storedata/aadhar_doc/', blank=True, null=True)
   imageofstore=models.FileField(upload_to='storedata/store_image/', blank=True, null=True)
   storeestablishment=models.DateField(null=True,blank=True)
   gstno=models.CharField(max_length=15,null=True,blank=True)
   hsnsac=models.CharField(null=True,blank=True,max_length=20)
   is_activee=models.IntegerField(default=1,null=True,blank=True)
   latitude = models.FloatField(blank=True, null=True)
   longitude = models.FloatField(blank=True, null=True)
   is_deleted=models.BooleanField(default=False,null=True,blank=True)




class usecategory(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   companyname=models.CharField(max_length=90)
   modelname=models.CharField(max_length=100)
   modelyear=models.IntegerField()
   active=models.BooleanField(default=True)

# class useincategory(models.Model):
#    usecategory=[
#       ('Car','Car'),
#       ('Bike','Bike'),
#    ]
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    usecategory=models.CharField(max_length=80)
#    wheretouse=models.CharField(max_length=100)

class productlisting(models.Model):
   store=models.ForeignKey(storedata, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   productname=models.CharField(max_length=100)
   productimage=models.ImageField(upload_to='storedata/product_image/', blank=True, null=True)
   usecategorylist=models.ForeignKey(usecategory,on_delete=models.CASCADE)
   # useincategory=models.CharField(max_length=100)
   productprice=models.IntegerField()
   modelyear=models.IntegerField()
   companyname=models.CharField(max_length=80)
   active=models.BooleanField(default=True)

