from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from .authentication import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
import os
import vk
import vk.exceptions
import uuid
import urllib.request
from django.conf import settings


class Auth(APIView):
    def post(self, request):
        vk_key = request.data['access_key']
        email = request.data['email']
        vk_id = int(request.data['vk_id'])

        try:
            session = vk.Session(access_token=vk_key)
            api = vk.API(session)
            profile = api.account.getProfileInfo()
            try:
                user = User.objects.get(photouser__vk_id=vk_id)
            except User.DoesNotExist:
                user = User(
                    username=str(uuid.uuid1()),
                    first_name=profile['first_name'],
                    last_name=profile['last_name'],
                    email=email,
                    password=vk_key,
                    is_active=True
                )
                user.save()
                user.photouser = PhotoUser(
                    user=user,
                    vk_id=vk_id,
                    vk_key=vk_key,
                )
                user.photouser.save()

        except vk.exceptions.VkAPIError:
            raise exceptions.AuthenticationFailed('Wrong VK key')

        if not user.photouser.avatar:
            vk_profile = api.users.get(fields="photo_200_orig,photo_100")[0]
            filepattern = "u%i.jpg" % vk_id
            urllib.request.urlretrieve(
                vk_profile['photo_200_orig'],
                os.path.join(settings.MEDIA_ROOT, "vkava", filepattern)
            )
            urllib.request.urlretrieve(
                vk_profile['photo_100'],
                os.path.join(settings.MEDIA_ROOT, "vkava", "thumb", filepattern)
            )
            user.photouser.avatar = os.path.join("vkava", filepattern)
            user.photouser.thumb = os.path.join("vkava", "thumb", filepattern)
            user.photouser.save()
        serializer = UserSerializer(user)

        return Response({
            "token": user.photouser.auth_token
        })


class Feed(APIView):
    authentication_classes = (VkAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        limit = int(request.GET.get("limit", 20))
        offset = int(request.GET.get("offset", 0))
        data = [FeedSerializer(post).data for post in Post.objects.all()][offset:offset+limit]
        return Response({
            "feed": data
        })


class UserList(generics.ListAPIView):
    authentication_classes = (VkAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound("Post was not found.")
        return Response({
            "post": FeedSerializer(post).data
        })

    def post(self, request):
        post = PostSerializer(data=request.data)
        if post.is_valid():
            post = post.save(user=request.user)

        return Response({
            "post": FeedSerializer(post).data
        })

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound("Post was not found.")

        serializer = PostSerializer(post, data=request.data)
        if post.is_valid():
            post = serializer.save(user=request.user)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound("Post was not found.")
        if post.user != request.user:
            raise exceptions.PermissionDenied("This post belongs to other user. Please check your account data")
        post.delete()

        return Response()


class PostLike(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound("Post was not found.")
        return Response({
            "is_liked": post.toggle_like(request.user),
        })


class PostCommentsView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound("Post was not found.")
        return Response({
            "comments": [FeedSerializer(post).data for comment in post.comment_set.all()]
        })


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound("Comment was not found.")
        return Response({
            "comment": ShortCommentSerializer(comment).data
        })

    def post(self, request):
        serializer = ShortCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user)

        return Response({
            "comment": ShortCommentSerializer(comment).data
        })

    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise exceptions.NotFound("Comment was not found.")

        serializer = ShortCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            comment = serializer.save( ser=request.user)

        return Response({
            "comment": ShortCommentSerializer(comment).data
        })

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise exceptions.NotFound("Post was not found.")
        if comment.user != request.user:
            raise exceptions.PermissionDenied("This post belongs to other user. Please check your account data")
        comment.delete()

        return Response()


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id=None):
        if not user_id:
            profile = request.user
        else:
            try:
                profile = User.objects.get(id=user_id)
            except Post.DoesNotExist:
                raise exceptions.NotFound("Profile was not found.")
        return Response({
            "profile": UserSerializer(profile).data
        })