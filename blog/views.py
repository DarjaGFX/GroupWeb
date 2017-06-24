# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password , check_password
from .models import *
from .forms import *
from django.http import JsonResponse , HttpResponseRedirect , HttpResponse
from json import JSONEncoder
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
            user = User.objects.get(username = Email)
            if check_password(password , user.password):
                return render(request , 'blog/post/list.html')
            else:
                return render(request , 'blog/panel/login.html' , {'form':form})
        except:
            return render(request , 'blog/post/detail.html')
    else:
        return render(request , 'blog/panel/login.html' , {'form':form})
    

# ########## #
# App Views# #
# ########## #


@csrf_exempt
def Narlogin(request):
    email = request.POST['email']
    PassWord = request.POST['npass']
    if is_Email_format(email):
        user = User.objects.filter(email= email.lower() )
        if len(user)>0 and check_password(PassWord , user[0].password):
            if user[0].is_active and user[0].is_authenticated():
                return JsonResponse({'Status':'0x0000','Token':members.objects.get(user = user[0]).Token, },encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x000F' },encoder=JSONEncoder)    
        else:
            return JsonResponse({'Status':'0x0001' },encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010' },encoder=JSONEncoder)
    
@csrf_exempt
@require_POST
def NarSignUp(request):
    PassWord = make_password(request.POST['npass'], hasher='default')
    email    = request.POST['nemail']
    dispusn  = request.POST['ndispn']
    if PassWord and dispusn :
        if is_Email_format(email):
            if is_Email_used(email):
                if User.objects.get(email = email).is_active:
                    return JsonResponse({'Status':'0x0002',},encoder=JSONEncoder)
                else:
                    return JsonResponse({'Status':'0x000F',},encoder=JSONEncoder)
            else:
                code = CreateToken()
                subject = 'فعال سازی اکانت ناردون'
                message = '.سلام {} عزیز \n برای فعال سازی اکانت ناردون خود روی لینک زیر کلیک کنید. چنانچه شما در ناردون ثبت نام نکرده اید این ایمیل را نادیده بگیرید \n {}'.format( dispusn , request.build_absolute_uri('/activate/')+'?ac='+code)
                fmail = 'ali.jafari20@gmail.com'
                send_mail(subject, message, fmail,[email])
                actv = activation.objects.create(email = email , code = code)
                new_user = User.objects.create_user(
                    username = email,
                    email = email ,
                    password = PassWord ,
                    first_name = dispusn
                    )
                new_user.is_active = False
                new_user.is_staff = False
                try:
                    gp = Group.objects.get(name = 'user')
                except Group.DoesNotExist:
                    Group.objects.create(name = 'user')
                    gp = Group.objects.get(name = 'user')
                new_user.groups.add(gp)
                new_user.save()
                new_member = members.objects.create(
                    user = new_user ,
                    Token = CreateToken() )
                try:
                    img = UploadProPicForm(request.POST, request.FILES)
                    if img.is_valid():
                        b4save = img.save(commit = False)
                        b4save.Token = new_member.Token
                        b4save.save()  
                        name, ext = str(request.FILES['propic']).replace(' ','_').split('.')
                        domain = request.build_absolute_uri('/blog/static/media/usr/{}/profilepicture/profile.'.format(new_member.Token)) + ext
                        new_member.ProPic = domain
                        new_member.save()
                except:
                    pass
                if new_user.is_authenticated():
                    return JsonResponse({'Status':'0x0000',},encoder=JSONEncoder)
                else:
                    return JsonResponse({'Status':'0x0003',},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0010',},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0006',}, encoder=JSONEncoder)


@csrf_exempt
def PostDetailView(request):
    postid = request.POST['id']
    post = Post.objects.filter(post_id = postid)
    if len(post)>0:
        result = dict()
        tmp = dict()
        coms = []
        comments = Comment.objects.filter(post = post[0] , active = True )
        if len(comments)>0:
            coms.clear()
            for cm in comments:
                response = dict()
                response.update({
                    'authorImg'    : str(cm.member.ProPic),
                    'Name'      : str(cm.member), 
                    'Text'      : cm.Text , 
                    'Date'      : str(cm.created.year)+'/'+str(cm.created.month)+'/'+str(cm.created.day) , 
                    'Time'      : str(cm.created.hour)+':'+str(cm.created.minute) 
                }) 
                coms.append(response)   
        result.update({'Comments':coms})
        return JsonResponse(result ,encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x000D'} ,encoder=JSONEncoder)

@csrf_exempt
def GroupPosts(request):
    gpname = request.POST['Group']
    group = NarGroups.objects.filter(Name = gpname)
    post = Post.objects.filter(Group = group , post_status = 'published' )
    result = dict()
    tmp = []
    i = len(post)
    for j in range(i-1,-1,-1):
        tpost = dict()
        tpost.update({
            'profile': str(post[j].author.ProPic),
            'Id'     : post[j].post_id , 
            'Image'  : post[j].ImageUrl ,
            'Title'  : post[j].Title ,
            'author' : post[j].author.DisplayUserName , 
            'Text'   : post[j].Text , 
            'Date'   : str(post[j].publish.year)+'/'+str(post[j].publish.month)+'/'+str(post[j].publish.day) , 
            'Time'   : str(post[j].publish.hour)+":"+str(post[j].publish.minute)
        }) 
        tmp.append(tpost)
    result.update({'Posts':tmp})
    return JsonResponse(result ,encoder=JSONEncoder)

@csrf_exempt
def fetchGroupNames(request):
    gp = NarGroups.objects.all()
    gps = []
    result = dict()
    if len(gp)>0:
        for g in gp:
            tmp = dict()
            tmp.update({ 
                'Name' : g.Name , 
                'logo' : g.logo
            })
            gps.append(tmp)
    result.update({'Groups':gps})
    return JsonResponse(result ,encoder=JSONEncoder)


@csrf_exempt
def addGroup(request):
    name = request.POST['Name'] 
    desc = request.POST['description']
    Token = request.POST['Token']
    user = members.objects.filter(Token = Token)
    if len(user) > 0:
        if str(user[0].user.groups.all()[0].name) == 'admin':
            if name !="" and desc != "":
                ngr , created = NarGroups.objects.get_or_create(Name = name , description = desc)
                try:
                    img = UploadlogoForm(request.POST, request.FILES)       
                    if img.is_valid():
                        img.save()  
                        domain = request.build_absolute_uri('/blog/static/media/GroupLogo/') + str(request.FILES['pic']).replace(' ','_')
                        #TODO: rename uploaded image to a meaningful name !
                    ngr.logo = domain
                except:
                    pass
                ngr.save()
                return JsonResponse({'Status':'0x0000'} ,encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x0006'} ,encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0007'} ,encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0004'} ,encoder=JSONEncoder)

@csrf_exempt
def addNewPost(request):
    Token = request.POST['Token']
    Title = request.POST['Title']
    Text = request.POST['Text']
    status = request.POST['status']
    mmber = members.objects.filter(Token = Token)
    if len(mmber)>0:
        if mmber[0].user.groups.all()[0].name != 'user':
            author = mmber[0]
            if Title is not "" and Text is not ""  and status is not "":
                if status is 'draft' or 'published':
                    chck = Post.objects.filter(author = author , Title = Title)
                    if len(chck)<1:
                        gp = request.POST['Group']
                        Group = NarGroups.objects.filter(Name = gp)
                        Today = jdatetime.datetime.now()
                        img = UploadPostImage_Form(request.POST, request.FILES)
                        domain = "https://"
                        if img.is_valid():
                            img.save()
                            domain += request.get_host()
                            domain += "/blog/static/media/post/{}/{}/{}/{}/{}/".format(Today.year,Today.ctime()[4:7],Today.day,Today.hour,Today.minute) + str(request.FILES['Image']).replace(' ','_')
                        pst = Post.objects.create(post_status = status ,Title = Title , author = author , Text = Text , ImageUrl=domain ,Group = Group[0] ,publish = Today)
                        return JsonResponse({'Status':'0x0000'} ,encoder=JSONEncoder)
                    else:
                        return JsonResponse({'Status':'0x0005'} ,encoder=JSONEncoder)
                else:
                    return JsonResponse({'Status':'0x000C'} ,encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x0006'} ,encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0007'} ,encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0004'} ,encoder=JSONEncoder)

@csrf_exempt
def addcomment(request):
    post_id = request.POST['PostId']
    Token = request.POST['Token']
    Text = request.POST['Text']
    user = members.objects.filter(Token = Token)
    post = Post.objects.filter(post_id = post_id)
    if len(user)>0:
        if len(post)>0:
            if Text != "":
                Comment.objects.get_or_create(post = post[0] , member = user[0] , Text = Text)
                return JsonResponse({'Status':'0x0000' },encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x0006' },encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0008' },encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0001' },encoder=JSONEncoder)

@csrf_exempt
def getAvailableGroups(request):
    Email = request.POST['Email']
    if is_Email_format(email):           
        if is_Email_used(email):
            us = User.objects.filter(email = Email.lower())
            user = members.objects.filter(user = us)
            res = dict()
            arr = []
            if len(user)>0:
                if user[0].user.groups.all()[0].name == 'user':
                    return JsonResponse({'Status':'0x0007'},encoder=JSONEncoder)
                elif user[0].user.groups.all()[0].name == 'member':
                    gp = GroupMembers.objects.filter(user = user[0])
                    for n in gp :
                        tmp = dict()
                        tmp.update({'Name':str(n.group) , 'Logo':n.logo})
                        arr.append(tmp)    
                elif user[0].user.groups.all()[0].name == 'admin':
                    ng = NarGroups.objects.all()
                    for n in ng :
                        tmp = dict()
                        tmp.update({'Name':n.Name, 'Logo':n.logo})
                        arr.append(tmp)
            else:
                return JsonResponse({'Status':'0x0004'},encoder=JSONEncoder)
            res.update({'Groups':arr})
            return JsonResponse(res,encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0000',},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010' },encoder=JSONEncoder)
@csrf_exempt
def setAvailableGroups(request):
    Token = request.POST['Token']
    admin = members.objects.filter(Token = Token)
    if len(admin)>0:
        if admin[0].user.groups.all()[0].name != 'admin':
            return JsonResponse({'Status':'0x0007'},encoder=JSONEncoder)
        else:
            un = request.POST['email']
            gp = request.POST['group']
            action = request.POST['action']
            if is_Email_format(email):           
                if is_Email_used(email):
                    if gp != "":
                        us = User.objects.get(email = un.lower())
                        user = members.objects.filter(user = us)
                        group = NarGroups.objects.filter(Name = gp)
                        if len(user)>0:
                            if len(group)>0:
                                if action == 'add':
                                    GroupMembers.objects.get_or_create(user = user[0] , group = group[0])
                                    return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
                                elif action == 'remove':
                                    x = GroupMembers.objects.filter(user = user[0] , group = group[0])
                                    x.delete()
                                    return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
                                else:
                                    return JsonResponse({'Status':'0x000B'},encoder=JSONEncoder)
                            else:
                                return JsonResponse({'Status':'0x000A'},encoder=JSONEncoder)
                        else:
                            return JsonResponse({'Status':'0x0009'},encoder=JSONEncoder)   
                    else:
                        return JsonResponse({'Status':'0x0006'},encoder=JSONEncoder)
                else:
                    return JsonResponse({'Status':'0x0000',},encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x0010' },encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0004'},encoder=JSONEncoder)

@csrf_exempt
def App_LoadProfile(request):
    Token = request.POST['Token']
    user = members.objects.filter(Token = Token)
    if len(user)>0:
        u = user[0]
        res = {'propic':u.ProPic ,'Email':u.user.email , 'dispun':u.user.first_name , 'AccessLevel':u.user.groups.all()[0].name}
        return JsonResponse(res,encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0004'},encoder=JSONEncoder)


@csrf_exempt
def App_MemberProfileView(request):
    postID = request.POST['postid']
    if postID != "":
        post = Post.objects.get(post_id = postID)
        u = post.author
        gps = GroupMembers.objects.filter(user = u)
        grp = []
        for g in gps:
            groups = dict()
            groups.update({'Name':g.group})
            grp.append(groups)
        res = {'propic':u.ProPic ,'Email':u.user.email , 'dispun':u.user.first_name , 'AccessLevel':u.user.groups.all()[0].name , 'Groups':grp}
        return JsonResponse(res,encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0006'},encoder=JSONEncoder)

@csrf_exempt
def App_EditProfile(request):
    Token = request.POST['Token']
    user = members.objects.filter(Token = Token)
    if len(user)>0:
        if user[0].user.is_active:
            u = user[0]
            arr = []
            try:
                img = UploadProPicForm(request.POST , request.FILES)  
                if img.is_valid():
                    s = img.save(commit = False)
                    uniqueID = CreateToken()
                    s.uniqueID = uniqueID
                    s.Token = Token
                    s.save()
                    name, ext = str(request.FILES['propic']).replace(' ','_').split('.')
                    u.ProPic =  request.build_absolute_uri('/blog/static/media/usr/{}/profilepicture/profile.{}.'.format(Token,uniqueID)) + ext
                    u.save()
                    tmp = {'ProfilePicture':'0x0000'}
                    arr.append(tmp)
            except:
                u.ProPic = ''
                u.save()
                tmp = {'ProfilePicture':'0x0003'}
                arr.append(tmp)
                
            try:
                newEmail = request.POST['email']
                if not is_Email_format(newEmail.lower()):
                    tmp = {'Email':'0x0006'}
                    arr.append(tmp)
                else:
                    if newEmail != u.email :
                        if is_Email_used(newEmail.lower()):
                            tmp = {'Email':'0x0002'}
                            arr.append(tmp)
                        else:
                            code = CreateToken()
                            subject = 'تغییر ایمیل اکانت ناردون'
                            message = '.سلام {} عزیز \n برای تغببر اکانت ناردون خود روی لینک زیر کلیک کنید. {}'.format( u.user.first_name , request.build_absolute_uri('/App/user/profile/acticate/')+'?ac='+code)
                            fmail = 'ali.jafari20@gmail.com'
                            send_mail(subject, message, fmail,[newEmail])
                            newmc = MailChange.objects.filter(primarymail= u.user.email , secondmail = newEmail.lower())
                            if len(newmc)>0:
                                newmc[0].code = code
                                newmc[0].save()
                            else:
                                MailChange.objects.create(code  = code ,primarymail= u.user.email , secondmail = newEmail.lower())
                            tmp = {'Email':'0x0000'}
                            arr.append(tmp)
                    else:
                        tmp = {'Email':'0x0000'}
                        arr.append(tmp)
            except:
                pass
            try:
                dispn = request.POST['dispun']
                if dispn == "":
                    tmp = {'DisplayUName':'0x0006'}
                    arr.append(tmp)
                else:
                    u.user.first_name = request.POST['dispun']
                    u.user.save()
                    tmp = {'DisplayUName':'0x0000'}
                    arr.append(tmp)
            except:
                pass
            try:
                if check_password(request.POST['OldPass'] , u.user.password):
                    pwd = request.POST['NewPass']
                    if pwd == "":
                        tmp = {'PassWord':'0x0006'}
                        arr.append(tmp)
                    else:
                        u.user.password = make_password(pwd , hasher='default')
                        u.user.save()
                        tmp = {'PassWord':'0x0000'}
                        arr.append(tmp)
                else:
                    tmp = {'PassWord':'0x000E'}
                    arr.append(tmp)
            except:
                pass
            u.save()
            return JsonResponse({'Status':arr},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x000F'},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0004'},encoder=JSONEncoder)

        
def activate(request):
    code = request.GET['ac']
    req = activation.objects.filter(code = code)
    if len(req)>0 :  # if code is in temporary db, read the data and create the user
        mmbr = User.objects.get(email = req[0].email)
        mmbr.is_active = True
        mmbr.save()
        req[0].delete()
        return JsonResponse({'message':'ok'},encoder=JSONEncoder)
    else:
        return JsonResponse({'message':'Activation link expired'},encoder=JSONEncoder)

def secondarymailactivate(request):
    code = request.GET['ac']
    updt = MailChange.objects.filter(code = code)
    if len(updt)>0:
        mbr = User.objects.get(email = updt[0].primarymail)
        mbr.email = updt[0].secondmail
        mbr.save()
        updt[0].delete()
        return JsonResponse({'message':'ok'},encoder=JSONEncoder)
    else:
        return JsonResponse({'message':'Activation link expired'},encoder=JSONEncoder)

@csrf_exempt
def MailAvailability(request):
    arg = request.POST['email']
    if is_Email_format(arg.lower()):
        if is_Email_used(arg.lower()):
            return JsonResponse({'Status':'0x0002'},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010'},encoder=JSONEncoder)

@csrf_exempt
def forget_pass_request(request):
    mail = request.POST['email']
    if is_Email_format(mail.lower()):
        if is_Email_used(mail.lower()):
            user = User.objects.filter(email = mail.lower())
            if not len(user)>0:
                return JsonResponse({'Status':'0x0009'},encoder=JSONEncoder)                
            elif not user[0].is_active:
                return JsonResponse({'Status':'0x000F'},encoder=JSONEncoder)                
            else:
                u = user[0]
                code = CreateToken()[:4].upper()
                subject = 'ریست پسورد اکانت ناردون'
                message = '.سلام {} عزیز \n برای ایجاد پسورد جدید از کد زیر استفاده کنید.\n {}'.format( u.first_name , code)
                fmail = 'ali.jafari20@gmail.com'
                send_mail(subject, message, fmail,[mail])
                newmc = forget_pass.objects.filter(email= u.email)
                if len(newmc)>0:
                    newmc[0].code = code
                    newmc[0].save()
                else:
                    forget_pass.objects.create(code  = code ,email= u.email)
                return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0009'},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010'},encoder=JSONEncoder)

@csrf_exempt
def change_forgotten_password(request):    
    mail = request.POST['email']
    code = request.POST['code']
    password = request.POST['password']
    if is_Email_format(mail.lower()):
        if is_Email_used(mail.lower()):
            u = User.objects.get(email = mail.lower())
            if code and password:
                req = forget_pass.objects.filter(code  = code ,email= u.email)
                if len(req)>0:
                    u.password = make_password(password , hasher='default' )
                    u.save()
                    req[0].delete()
                    return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
                else:
                    return JsonResponse({'Status':'0x0013'},encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x0006'},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0009'},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010'},encoder=JSONEncoder)

@csrf_exempt
def check_forgotten_password_code(request):
    mail = request.POST['email']
    code = request.POST['code']
    if is_Email_format(mail.lower()):
        if is_Email_used(mail.lower()):
            u = User.objects.get(email = mail.lower())
            if code:
                req = forget_pass.objects.filter(code  = code ,email= u.email)
                if len(req)>0:
                    return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
                else:
                    return JsonResponse({'Status':'0x0013'},encoder=JSONEncoder)
            else:
                return JsonResponse({'Status':'0x0006'},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0009'},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010'},encoder=JSONEncoder)


@csrf_exempt
def resend_veriffication_mail(request):
    mail = request.POST['email']
    mail = mail.lower()
    if is_Email_format(mail):
        if is_Email_used(mail):
            mmbr = User.objects.get(email = mail)
            if mmbr.is_active:
                return JsonResponse({'Status':'0x0011'},encoder=JSONEncoder)
            else:
                code = CreateToken()
                subject = 'فعال سازی اکانت ناردون'
                message = '.سلام {} عزیز \n برای فعال سازی اکانت ناردون خود روی لینک زیر کلیک کنید. چنانچه شما در ناردون ثبت نام نکرده اید این ایمیل را نادیده بگیرید \n {}'.format( mmbr.DisplayUserName , request.build_absolute_uri('/activate/')+'?ac='+code)
                fmail = 'ali.jafari20@gmail.com'
                send_mail(subject, message, fmail,[mail])
                actv = activation.objects.filter(email = mail)
                if len(actv)>0:
                    actv[0].code = code
                    actv[0].save()
                else:
                    activation.objects.create(email = mail , code = code)
                return JsonResponse({'Status':'0x0000'},encoder=JSONEncoder)
        else:
            return JsonResponse({'Status':'0x0009'},encoder=JSONEncoder)
    else:
        return JsonResponse({'Status':'0x0010'},encoder=JSONEncoder)
