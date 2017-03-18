from django.shortcuts import render, get_object_or_404
from .models import Post , Comment,render
#from .forms import loginForm


def post_list(request):
    posts = Post.objects.filter(post_status = "published")
    return render(request , 'blog/post/list.html' , {'posts':posts})

def post_detail(request,idd):
    post = Post.objects.filter(post_id = idd)
    comments = Comment.objects.filter(active = True , postID = post[0].post_id )
    return render(request,'blog/post/detail.html',{'post':post[0],'comments':comments})
