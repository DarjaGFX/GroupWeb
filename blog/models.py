from __future__ import unicode_literals
from django.contrib.auth.models import User , Group
import datetime
from django.db import models

class NarGroups(models.Model):
    Name = models.CharField(max_length=150 , unique = True)
    description = models.TextField()
    def __str__(self):
        return self.Name

class Token(models.Model):
    token = models.CharField(max_length = 50)
    #user  = models.OneToOneField(members , on_delete = models.CASCADE)
    def __str__(self):
        return "{}_token".format(self.user)

class members(models.Model):
    Group           = models.ForeignKey(NarGroups)
    email           = models.EmailField(null = False)
    userName        = models.CharField(max_length=32 , unique = True, null = False)
    password        = models.CharField(max_length=32 , null = False)
    DisplayUserName = models.CharField(max_length = 15 , null = False)
    def __str__(self):
        return self.DisplayUserName

class Post(models.Model):
    status      = (('draft', 'Draft'),('published','Published'))
    post_id     = models.AutoField(primary_key=True)
    post_status = models.CharField(max_length = 10 , choices = status , default ='draft')
    author      = models.ForeignKey(members , related_name = 'blog_posts', on_delete = models.CASCADE)
    Title       = models.CharField(max_length = 250)
    slug        = models.SlugField(max_length = 250 , unique_for_date='publish')
    Text        = models.TextField()
    publish     = models.DateTimeField(default = datetime.datetime.now)
    created     = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)
    like        = models.BigIntegerField(default=0)
    disLike     = models.BigIntegerField(default=0)

    def __str__(self):
        return self.Title
    class Meta:
        ordering = ('-publish',)

class Comment(models.Model):
    postID  = models.ForeignKey(Post,related_name="post_comments")
    name    = models.CharField(max_length=80)
    email   = models.EmailField()
    Text    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)
    like    = models.BigIntegerField(default=0)
    disLike = models.BigIntegerField(default=0)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.postID)
