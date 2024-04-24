from django.db import models

from adminh.models import User


# Create your models here.

class servicestoredata(models.Model):
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
   storelicencedocument=models.FileField(upload_to='servicestoredata/licence_doc/', blank=True, null=True)
   ownersdocument=models.FileField(upload_to='servicestoredata/aadhar_doc/', blank=True, null=True)
   imageofstore=models.FileField(upload_to='servicestoredata/servicestore_image/', blank=True, null=True)
   storeestablishment=models.DateField(null=True,blank=True)
   gstno=models.CharField(max_length=15,null=True,blank=True)
   hsnsac=models.CharField(null=True,blank=True,max_length=20)
   is_activee=models.IntegerField(default=1,null=True,blank=True)
   is_deleted=models.BooleanField(default=False,null=True,blank=True)


class servicelisting(models.Model):
   store=models.ForeignKey(servicestoredata, on_delete=models.CASCADE)
   towable=models.BooleanField(default=0)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   avgtime=models.CharField(max_length=60)
   servicename=models.CharField(max_length=80)
   serviceimage=models.FileField(upload_to='servicestoredata/service_image/')
   serviceprice=models.IntegerField()
   active=models.BooleanField(default=True)

