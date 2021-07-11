from django.contrib import admin
from .models import Post, Group




class PostAdmin(admin.ModelAdmin):
    """Class to make different View in DjangoAdmin"""
    list_display = ('text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = "--" 


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    

admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)