from django.conf.urls import url
from . import views , AppView

urlpatterns = [
    url(r'^activate/', AppView.activate , name = 'activate'),
    url(r'^App/user/profile/ForgetPass/', AppView.forget_pass_request , name = 'forget_pass_request'),
    url(r'^App/user/profile/activate/', AppView.secondarymailactivate , name = 'secondarymailacticate'),
    url(r'^App/user/profile/reactivate/', AppView.resend_veriffication_mail , name = 'resend_veriffication_mail'),
    url(r'^App/user/profile/ChangeForgetPass/', AppView.change_forgotten_password , name = 'change_forgotten_password'),
    
    # WebSite views
    url(r'^$', views.post_list , name = 'post_list'),
    url(r'^(?P<idd>\d+)/$',views.post_detail, name = 'post_detail'),
    url(r'^accounts/login/$',views.login_panel, name = 'login_panel'),
    url(r'^accounts/logout/$',views.logout, name = 'logout'),
    url(r'^panel/$', views.load_panel , name = 'load_panel'),
    
    
    
    ####################
    # Remote App Views!#
    url(r'^App/PostView/' , AppView.GroupPosts , name = 'GroupPosts'),
    url(r'^App/Post/set/' , AppView.addNewPost , name = 'addNewPost'),
    
    url(r'^App/signup/', AppView.NarSignUp , name = 'NarSignUp'),
    url(r'^App/login/', AppView.Narlogin , name = 'Narlogin'),
    
    url(r'^App/Comments/get/', AppView.PostDetailView , name = 'PostDetailView'),
    url(r'^App/Comments/set/' , AppView.addcomment , name = 'addcomment'),
    
    url(r'^App/Group/get/', AppView.fetchGroupNames , name = 'fetchGroupNames'),
    url(r'^App/Group/add/', AppView.addGroup , name = 'addGroup'),
    url(r'^App/Group/set/', AppView.App_EditGroup , name = 'App_EditGroup'),
    
    url(r'^App/user/groups/get/' , AppView.getAvailableGroups , name = 'getAvailableGroups'),
    url(r'^App/user/groups/set/' , AppView.setAvailableGroups , name = 'setAvailableGroups'),
    
    url(r'^App/user/profile/get/' , AppView.App_LoadProfile , name = 'App_LoadProfile'),
    url(r'^App/user/profile/member/' , AppView.App_MemberProfileView , name = 'App_MemberProfileView'),
    url(r'^App/user/profile/set/' , AppView.App_EditProfile , name = 'App_EditProfile'),

    url(r'^App/check/mail/', AppView.MailAvailability , name = 'MailAvailability'),
    url(r'^App/check/ForgetCode/', AppView.check_forgotten_password_code , name = 'check_forgotten_password_code'),
    # url(r'^App/email/' , views.test , name = 'test'),
    #url(r'^add/group/', views.addGroup , name = 'addGroup'),
    #url(r'^$', views.postListView.as_view(), name= 'post_list'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{1})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail, name = 'post_detail'),
    #url(r'^(?P<post>[-\w]+)/$', views.post_detail , name = 'post_detail'),
]
