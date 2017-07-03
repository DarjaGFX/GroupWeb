# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password , check_password
from .models import *
from .forms import *
from django.http import JsonResponse , HttpResponseRedirect , HttpResponse
from json import JSONEncoder
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.core.validators import validate_email
import uuid
import jdatetime


def CreateToken():
    newToken = str(uuid.uuid4())[:23].replace('-','').lower()
    try:
        tokenExists = members.objects.get(Token = newToken)
        # andMayBeHere = activation.objects.get(code = newToken)
        CreateToken()
    except:
        return newToken

def is_Email_format(mail):
    arg = str(mail).lower()
    try:
        if validate_email(arg) == None:
            return True
    except:
        return False

def is_Email_used(mail):
    arg = str(mail).lower()
    user = User.objects.filter(email = arg)
    if len(user)>0:
        return True
    else:
        return False

############################################################
def post_list(request):
    posts = Post.objects.filter(post_status = "published")
    return render(request , 'blog/post/list.html' , {'posts':posts})

def singup(request):
    form = form_SignUp()
    return render(request , "blog/base.html" , {"form":form})

def addGroupform(request):
    form = form_Group()
    # if form.is_valid():
    return render(request , "blog/base.html" , {"form":form})

def post_detail(request,idd):
    post = Post.objects.filter(post_id = idd)
    comments = Comment.objects.filter(active = True , post = post[0] )
    form  = form_comment(request.POST or None)
    if form.is_valid():
        Token = form.cleaned_data['Token']
        text = form.cleaned_data['Text']
        mmbr = members.objects.filter(Token = Token)
        post = Post.objects.filter(post_id = idd)
        new_comment , created = Comment.objects.get_or_create( member = mmbr , Text = text , post = post[0] )
    return render(request,'blog/post/detail.html',{'post':post[0],'comments':comments , 'form':form})

@csrf_exempt
def login_panel(request):
    form = form_login(request.POST or None)
    if form.is_valid():
        Email = form.cleaned_data['user']
        password = form.cleaned_data['password']
        try:
            user = auth.authenticate(username=Email, password=password)
            if user != None:
                auth.login(request, user)
                nextpage = request.GET['next']
                if nextpage!= "" and nextpage != "/accounts/logout/":
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return render(request , 'blog/panel/panel.html' , {'form':form})
            else:
                return render(request , 'blog/panel/login.html' , {'form':form})
        except:
            return render(request , 'blog/panel/login.html' , {'form':form})
    else:
        return render(request , 'blog/panel/login.html' , {'form':form})

def logout(request):
    auth.logout(request)
    form = form_login(request.POST or None)
    return load_panel(request)


@login_required
def load_panel(request):
    user = User.objects.get(email = request.user)
    mmbr = members.objects.get(user = user)
    return render(request , 'blog/panel/panel.html' , {'Name':request.user.first_name,
                                                       'ProPic':mmbr.ProPic
                                                    })
    