from django.conf.urls import url
from . import views

urlpatterns = [
    # WebSite views
    url(r'^$', views.post_list , name = 'post_list'),
    url(r'^(?P<idd>\d+)/$',views.post_detail, name = 'post_detail'),
    
    
    
    ####################
    # Remote App Views!#
    url(r'^App/PostView/' , views.GroupPosts , name = 'GroupPosts'),
    url(r'^App/Post/set/' , views.addNewPost , name = 'addNewPost'),
    
    url(r'^App/signup/', views.NarSignUp , name = 'NarSignUp'),
    url(r'^App/login/', views.Narlogin , name = 'Narlogin'),
    
    url(r'^App/Comments/get/', views.PostDetailView , name = 'PostDetailView'),
    url(r'^App/Comments/set/' , views.addcomment , name = 'addcomment'),
    
    url(r'^App/Group/get/', views.fetchGroupNames , name = 'fetchGroupNames'),
    url(r'^App/Group/set/', views.addGroup , name = 'addGroup'),
    
    url(r'^App/user/groups/get/' , views.getAvailableGroups , name = 'getAvailableGroups'),
    url(r'^App/user/groups/set/' , views.setAvailableGroups , name = 'setAvailableGroups'),
    url(r'^App/user/profile/get/' , views.App_LoadProfile , name = 'App_LoadProfile'),
    url(r'^App/user/profile/member/' , views.App_MemberProfileView , name = 'App_MemberProfileView'),

    #url(r'^add/group/', views.addGroup , name = 'addGroup'),
    #url(r'^$', views.postListView.as_view(), name= 'post_list'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{1})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail, name = 'post_detail'),
    #url(r'^(?P<post>[-\w]+)/$', views.post_detail , name = 'post_detail'),
]
