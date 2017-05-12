from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.http import JsonResponse 
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def Narlogin(request):
    UserName = request.POST['nuser']
    PassWord = request.POST['npass']
    user = members.objects.filter(userName= UserName ,password = PassWord)
    if len(user)>0:
        return JsonResponse({'Status':'OK','Token':user[0].Token, },encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'FAILED','ERROR':'0x0001' },encoder=JSONEncoder)

@csrf_exempt
def NarSignUp(request):
    UserName = request.POST['nuser']
    PassWord = request.POST['npass']
    email    = request.POST['nemail']
    dispusn  = request.POST['ndispn']
    grp      = request.POST['ngroup']
    ngroup = NarGroups.objects.filter(Name = grp)

    user = members.objects.filter(userName= UserName)
    if len(user)>0:
        return JsonResponse({'Status':'FAILED','ERROR':'0x0002', },encoder=JSONEncoder)
    else:
        new_member , created = members.objects.get_or_create(email=email , userName = UserName , password = PassWord , DisplayUserName = dispusn , Group = ngroup[0] )
        if created:
            return JsonResponse({'Status':'FAILED','ERROR':'0x0001' },encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'FAILED','Message':'unexpected error accured!',}, encoder=JSONEncoder)