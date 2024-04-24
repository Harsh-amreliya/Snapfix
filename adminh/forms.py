from django import forms
from .models import User
from stores.models import storedata

class storedetail(forms.ModelForm):
    class Meta:
        model=storedata
        fields=['email','user']


