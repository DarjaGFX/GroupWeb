# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.http import JsonResponse 
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.views.decorators.http import require_POST

def CreateToken():
    newToken = str(uuid.uuid4())[:23].replace('-','').lower()
    try:
        tokenExists = members.objects.get(Token = newToken)
        CreateToken()
    except:
        return newToken

def post_list(request):
    posts = Post.objects.filter(post_status = "published")
    return render(request , 'blog/post/list.html' , {'posts':posts})

def singup(request):
    form = form_SignUp()
    return render(request , "blog/base.html" , {"form":form})

def addGroup(request):
    form = form_Group()
    # if form.is_valid():
    return render(request , "blog/base.html" , {"form":form})
    
def post_detail(request,idd):
    post = Post.objects.filter(post_id = idd)
    comments = Comment.objects.filter(active = True , postID = post[0].post_id )
    form  = form_comment(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        text = form.cleaned_data['Text']
        postid = Post.objects.filter(post_id = idd)
        new_comment , created = Comment.objects.get_or_create(email=email , name = name , Text = text , postID = postid[0] )
    return render(request,'blog/post/detail.html',{'post':post[0],'comments':comments , 'form':form})



# ########## #
# App Views# #
# ########## #


@csrf_exempt
def Narlogin(request):
    UserName = request.POST['nuser']
    PassWord = request.POST['npass']
    user = members.objects.filter(userName= UserName.lower() ,password = PassWord)
    if len(user)>0:
        return JsonResponse({'Status':'0x0000','Token':user[0].Token, },encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0001' },encoder=JSONEncoder)

@csrf_exempt
@require_POST
def NarSignUp(request):
    UserName = request.POST['nuser']
    PassWord = request.POST['npass']
    email    = request.POST['nemail']
    dispusn  = request.POST['ndispn']
    grp      = request.POST['ngroup']
    #TODO: check if any empty parameters passed, return Error!
    ngroup = NarGroups.objects.filter(Name = grp)

    user = members.objects.filter(userName= UserName.lower())
    if len(user)>0:
        return JsonResponse({'Status':'0x0002',},encoder=JSONEncoder)
    else:
        new_member , created = members.objects.get_or_create(email=email , userName = UserName.lower() , password = PassWord , DisplayUserName = dispusn , Group = ngroup[0] , Token = CreateToken() )
        if created:
            return JsonResponse({'Status':'0x0000',},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0003',}, encoder=JSONEncoder)


@csrf_exempt
def loadComment(request):
    request.encoding = 'koi8-r'
    postid = request.POST['id']
    post = Post.objects.filter(post_id = postid)
    comments = Comment.objects.filter(postID = post[0] , active = True )
    if len(comments)>0:
        result = dict()
        coms = []
        for cm in comments:
            response = dict()
            response.update({'Name' : cm.name , 'Text' : cm.Text , 'Time' : str(cm.created.year)+'/'+str(cm.created.month)+'/'+str(cm.created.day) }) 
            coms.append(response)   
        result.update({'Comments':coms})
        return JsonResponse(result ,encoder=JSONEncoder)


@csrf_exempt
def fetchGroupNames(request):
    gp = NarGroups.objects.all()
    if len(gp)>0:
        result = dict()
        gps = []
        for g in gp:
            tmp = dict()
            tmp.update({ 'Name' : g.Name })
            gps.append(tmp)
        result.update({'Groups':gps})
        return JsonResponse(result ,encoder=JSONEncoder)