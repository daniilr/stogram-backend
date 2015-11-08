from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import hashlib
import uuid
import os
import time
from sorl.thumbnail import get_thumbnail


class PhotoUser(models.Model):
    thumb = models.ImageField(upload_to='ava/thumb/', null=True, blank=True)
    avatar = models.ImageField(upload_to='ava/', null=True, blank=True)
    user = models.OneToOneField(User)
    vk_id = models.IntegerField(null=True, blank=True)
    vk_key = models.CharField(max_length=128, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=120, null=True, blank=True)
    auth_token = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        token = str(settings.SECRET_KEY + self.user.username + str(time.time())).encode("utf-8")
        self.auth_token = hashlib.sha256(token).hexdigest()
        super(PhotoUser, self).save(*args, **kwargs)


class Like(models.Model):
    post = models.ForeignKey("Post")
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ("post", "user")

class Post(models.Model):
    origin = models.ImageField(upload_to='o/', blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_created=True)
    likes_count = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    def get_thumb(self):
        return get_thumbnail(settings.MEDIA_ROOT + self.origin.url, "256x256", crop="center")

    def toggle_like(self, user):
        try:
            like = self.like_set.get(user=user)
            like.delete()
            self.likes_count -= 1
            self.save()
            return True
        except Like.DoesNotExist:
            self.like_set.create(user=user)
            self.likes_count += 1
            self.save()
            return False


class Comment(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_created=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)

class Template(models.Model):
    name = models.CharField(max_length=200)
    origin = models.ImageField(upload_to='tpl/', blank=True, null=True)
