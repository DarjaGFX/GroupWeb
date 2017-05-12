from django.conf.urls import url
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.post_list , name = 'post_list'),
    #url(r'^$', views.postListView.as_view(), name= 'post_list'),
    url(r'^signup/', views.NarSignUp , name = 'NarSignUp'),
    url(r'^login/', views.Narlogin , name = 'Narlogin'),
    url(r'^add/group/', views.addGroup , name = 'addGroup'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{1})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail, name = 'post_detail'),
    url(r'^(?P<idd>\d+)/$',views.post_detail, name = 'post_detail'),
    #url(r'^(?P<post>[-\w]+)/$', views.post_detail , name = 'post_detail'),
]
