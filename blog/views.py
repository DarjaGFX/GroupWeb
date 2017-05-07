from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *

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
