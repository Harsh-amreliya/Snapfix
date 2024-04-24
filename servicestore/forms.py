from django import forms
from . import models

class addservicestoreform(forms.ModelForm):
    class Meta:
        exclude= ['user']
        model = models.servicestoredata
        fields='__all__'

class addservice(forms.ModelForm):
    class Meta:
        exclude=['user','store']
        model=models.servicelisting
        fields='__all__'

