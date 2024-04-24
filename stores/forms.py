from django import forms
from . import models

class addstoreform(forms.ModelForm):
    class Meta:
        exclude= ['user']
        model = models.storedata
        fields='__all__'

class addusecategory(forms.ModelForm):
    class Meta:
        exclude= ['user']
        model=models.usecategory
        fields='__all__'

# class adduseincategory(forms.ModelForm):
#     class Meta:
#         exclude = ['user']
#         model=models.useincategory
#         fields='__all__'

class addproduct(forms.ModelForm):
    class Meta:
        exclude = ['user','store']
        model=models.productlisting
        fields='__all__'