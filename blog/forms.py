from django import forms

from .models import *

class Group(forms.ModelForm):
    class Meta:
        model = NarGroups
        fields = ["Name","description"]

class SignUp(forms.ModelForm):
    class Meta:
        model = members
        fields = ["Group","email","userName","password","DisplayUserName"]