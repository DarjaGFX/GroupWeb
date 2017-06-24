from django import forms 
from django.forms import PasswordInput
from .models import *

class form_Group(forms.ModelForm):
    class Meta:
        model  = NarGroups
        fields = ['Name','description']

class form_SignUp(forms.Form):
    user    = models.ForeignKey(User , related_name = 'member_user' , on_delete = models.CASCADE)
    Token   = models.CharField(max_length=20 , unique = True , default = CreateToken() )
    propic  = models.ImageField()

class form_login(forms.Form):
    user            = forms.CharField(max_length = 30 , label ='نام کاربری')
    password        = forms.CharField(max_length = 30 , label ='رمز عبور' , widget = PasswordInput) 
    class Meta:
        fields = ['user','password']
       
class form_comment(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['Text']