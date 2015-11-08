from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import datetime
from PIL import Image

class UnixEpochDateField(serializers.DateTimeField):
    def to_representation(self, value):
        """ Return epoch time for a datetime object or ``None``"""
        import time
        try:
            return int(time.mktime(value.timetuple()))
        except (AttributeError, TypeError):
            return None

    def to_internal_value(self, value):
        import datetime
        return datetime.datetime.fromtimestamp(int(value))


class UserSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="photouser.status")
    url = serializers.CharField(source="photouser.url")
    thumb_photo = serializers.ImageField(source="photouser.thumb")
    origin_photo = serializers.ImageField(source="photouser.avatar")

    class Meta:
        model = User
        fields = ('id', 'last_name', 'status', 'first_name', "url", 'thumb_photo', 'origin_photo')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    created = UnixEpochDateField()
    updated = UnixEpochDateField()

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created', 'updated', 'user')


class ShortCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('body',)


class FeedSerializer(serializers.ModelSerializer):
    created = UnixEpochDateField()
    updated = UnixEpochDateField()
    user = UserSerializer()
    comments = CommentSerializer(source="comment_set", many=True)
    thumb = serializers.ImageField(source="get_thumb")

    class Meta:
        model = Post
        fields = ('id', 'body', 'thumb', 'origin', 'created', 'updated', 'likes_count', 'user', 'comments')
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('origin', 'body')

    def create(self, validated_data):
        validated_data['user'] = validated_data['user']
        return Post.objects.create(**validated_data)


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('origin', 'name', 'id')
