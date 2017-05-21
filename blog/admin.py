from django.contrib import admin
from .models import members, Post ,NarGroups , Comment

class Group_admin(admin.ModelAdmin):
    list_display = ('Name','description')

class Post_admin(admin.ModelAdmin):
    list_display  		= ('author' , 'Title', 'publish')
    list_filter 		= ('post_status','created','publish','author')
    search_fields 		= ('Title','Text')
    #prepopulated_fields = {'slug':('Title',)}
    date_hierarchy 		= 'publish'
    raw_id_fields 		= ('author',)
    ordering 			= ['post_status' , 'publish']

class CommentAdmin(admin.ModelAdmin):
    list_display	= ('member','created','active')
    raw_id_fields 		= ('post',)
admin.site.register(members)
admin.site.register(Post,Post_admin)
admin.site.register(NarGroups,Group_admin)
admin.site.register(Comment,CommentAdmin)