from django.contrib import admin

from .models import Post


class AdminPost(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug', 'author', 'created', 'modified']


admin.site.register(Post, AdminPost)




