from __future__ import unicode_literals
from django.contrib.auth.models import User , Group
import datetime
from django.db import models
from django.forms import ModelForm
from django_jalali.db import models as jmodels
import jdatetime
import uuid

def CreateToken():
    newToken = str(uuid.uuid4())[:23].replace('-','').lower()
    return newToken

def pro_pic_dir(instance, filename):
    name, ext = filename.split('.')
    file_path = 'blog/static/media/usr/{}/profilepicture/profile.{}'.format(instance.Token,ext) 
    return file_path

def post_img_dir(instance, filename):
    name, ext = filename.split('.')
    file_path = 'blog/static/media/usr/{}/posts/{}/img.{}'.format(instance.author,instance.post_id,ext) 
    return file_path

def group_logo_dir(instance, filename):
    name, ext = filename.split('.')
    file_path = 'blog/static/media/GroupLogo/{}/logo.{}'.format(instance.Name,ext) 
    return file_path

class GroupLogo(models.Model):
    Name = models.CharField(max_length=150 , null = False )
    pic = models.ImageField("Image", upload_to=group_logo_dir)
    upload_date= jmodels.jDateTimeField(auto_now_add =True)

class ProfilePicture(models.Model):
    Token        = models.CharField(max_length=20 , default = 1 )
    propic       = models.ImageField("Image", upload_to= pro_pic_dir )
    upload_date  = jmodels.jDateTimeField(auto_now_add =True)
        
class PostImage(models.Model):
    author_token  = models.CharField(max_length=20 , default =1)
    post_id       = models.AutoField(primary_key=True)
    Image         = models.ImageField("Image",upload_to =post_img_dir)
    upload_date   = jmodels.jDateTimeField(auto_now_add =True)
    
class UploadlogoForm(ModelForm):
    class Meta:
        model = GroupLogo
        fields = ['pic']

class UploadProPicForm(ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ['propic']

class UploadPostImage_Form(ModelForm):
    class Meta:
        model = PostImage
        fields = ['Image']

class NarGroups(models.Model):
    Name = models.CharField(max_length=150 , null = False , unique = True , verbose_name = "نام" )
    description = models.TextField(verbose_name = "توضیحات")
    logo = models.TextField(null = True , blank=True)
    def __str__(self):
        return self.Name

class members(models.Model):
    status          = (('user', 'User'),('member','Member'),('admin','Admin'))
    Token           = models.CharField(max_length=20 , unique = True , default = CreateToken() )
    ProPic          = models.TextField(null = True , blank=True)
    AccessLevel     = models.CharField(max_length = 10 , choices = status , default ='user' , verbose_name = "سطح کاربری")
    email           = models.EmailField(null = False , blank=False, unique = True , verbose_name = "ایمیل")
    password        = models.CharField(max_length=100 , null = False , verbose_name = "کلمه عبور")
    DisplayUserName = models.CharField(max_length = 15 , null = False , verbose_name = "نام کاربری نمایشی")
    created         = jmodels.jDateTimeField(auto_now_add = True)
    active          = models.BooleanField(default= False)
    def __str__(self):
        return self.DisplayUserName
    class Meta:
        unique_together = ("email", "Token",)

class activation(models.Model):
    email = models.EmailField(null = False , unique = True )
    code  = models.CharField(max_length=20 , unique = True , default = CreateToken())
    class Meta:
        unique_together = ("email", "code",)

class MailChange(models.Model):
    primarymail = models.EmailField(null = False)
    secondmail = models.EmailField(null = False)
    code  = models.CharField(max_length=20 , unique = True , default = CreateToken())
    class Meta:
        unique_together = ("primarymail", "secondmail",)

class forget_pass(models.Model):
    email = models.EmailField(null = False , unique = True )
    code  = models.CharField(max_length=20 , unique = True , default = CreateToken())

class GroupMembers(models.Model):
    user    = models.ForeignKey( members , related_name = 'Group_users' , on_delete = models.CASCADE)
    group   = models.ForeignKey( NarGroups , related_name = 'User_groups' , on_delete = models.CASCADE)
    class Meta:
        unique_together = ("group", "user",)

class Post(models.Model):
    status      = (('draft', 'Draft'),('published','Published'))
    post_id     = models.AutoField(primary_key=True)
    post_status = models.CharField(max_length = 10 , choices = status , default ='draft', verbose_name = "وضعیت")
    author      = models.ForeignKey(members , related_name = 'blog_posts', on_delete = models.CASCADE , verbose_name = "نویسنده")
    Title       = models.CharField(max_length = 250, verbose_name = "عنوان")
    Text        = models.TextField(verbose_name = "متن")
    ImageUrl    = models.TextField(null = True , blank = True)
    Group       = models.ForeignKey(NarGroups , default= "عمومی" , related_name = 'group_posts' , verbose_name = "گروه")
    publish     = jmodels.jDateTimeField(default = jdatetime.datetime.now, verbose_name = "تاریخ انتشار")
    created     = jmodels.jDateTimeField(auto_now_add = True)
    updated     = jmodels.jDateTimeField(auto_now = True)

    def __str__(self):
        return self.Title
    class Meta:
        ordering = ('-publish',)


class Comment(models.Model):
    post    = models.ForeignKey(Post,related_name="post_comments")
    member  = models.ForeignKey(members, verbose_name = "نام")
    Text    = models.TextField(verbose_name = "متن")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    active  = models.BooleanField(default= False)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return 'نوشته شده توسط {} در {}'.format(self.member,self.post)