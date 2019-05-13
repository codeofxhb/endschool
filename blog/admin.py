from django.contrib import admin
from .models import Blog, Blogtype

@admin.register(Blogtype)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'typename',)
    ordering = ('id',)

'''
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('blog', 'read_num')
    ordering = ('blog',)
'''

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''
        list_display = ('title', 'author', 'create_time', 'update_time', 'blogtype', 'get_read_num')
    '''
    list_display = ('id', 'title', 'author', 'create_time', 'update_time', 'blogtype', 'get_read_num', 'content')
    ordering = ('id',)

