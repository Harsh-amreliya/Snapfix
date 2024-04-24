from django import forms
from . import models

class liststorerequestform(forms.ModelForm):
    class Meta:
        model = models.liststorerequest
        fields='__all__'

class cartform(forms.ModelForm):
    class Meta:
        model = models.mycart
        fields='__all__'
        exclude=('user','productid','serviceid','quantity')

class towingrequestform(forms.ModelForm):
    class Meta:
        model = models.towingrequest
        fields='__all__'
        exclude=['user','storeid,','serviceid']

class productrequestform(forms.ModelForm):
    class Meta:
        model = models.productrequest
        fields='__all__'
        exclude=['user','storeid,','productid']