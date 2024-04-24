from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_admin=models.BooleanField('Is admin', default=False)
    is_store_owner=models.BooleanField('Is store owner', default=False)
    is_service_store_owner=models.BooleanField('Is service store owner', default=False)