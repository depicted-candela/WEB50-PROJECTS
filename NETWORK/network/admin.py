from django.contrib import admin
from .models import Post, Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'posting_time', 'text')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('get_following', 'follower')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)