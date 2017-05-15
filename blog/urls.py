from django.conf.urls import url
from . import views

urlpatterns = [
    # WebSite views
    url(r'^$', views.post_list , name = 'post_list'),
    url(r'^(?P<idd>\d+)/$',views.post_detail, name = 'post_detail'),
    
    
    
    ####################
    # Remote App Views!#
    url(r'^App/signup/', views.NarSignUp , name = 'NarSignUp'),
    url(r'^App/login/', views.Narlogin , name = 'Narlogin'),
    url(r'^App/PostDetailView/', views.PostDetailView , name = 'PostDetailView'),
    url(r'^App/Group/load/', views.fetchGroupNames , name = 'fetchGroupNames'),
    url(r'^App/Group/add/', views.addGroup , name = 'addGroup'),
    url(r'^App/upload/', views.home , name = 'home'),
    
    
    #url(r'^add/group/', views.addGroup , name = 'addGroup'),
    #url(r'^$', views.postListView.as_view(), name= 'post_list'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{1})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail, name = 'post_detail'),
    #url(r'^(?P<post>[-\w]+)/$', views.post_detail , name = 'post_detail'),
]
