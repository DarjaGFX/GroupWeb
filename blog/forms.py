from django import forms
from .models import *

class form_Group(forms.ModelForm):
    class Meta:
        model  = NarGroups
        fields = ['Name','description']

# class form_SignUp(forms.ModelForm):
#     class Meta:
#         model  = members
#         fields = ["email","password","DisplayUserName"]

class form_comment(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['Text']