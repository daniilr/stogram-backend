from django.contrib import admin
from .models import Post, PhotoUser, Comment, Template

admin.site.register(Post)
admin.site.register(Template)
admin.site.register(PhotoUser)
admin.site.register(Comment)
