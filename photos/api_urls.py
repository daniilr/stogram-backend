from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url('^auth/$', Auth.as_view()),
    url('^feed/$', Feed.as_view()),
    url('^users/list/$', UserList.as_view()),
    url('^post/$', PostView.as_view()),
    url('^profile/$', ProfileView.as_view()),
    url('^profile/(?P<user_id>\d+)/$', ProfileView.as_view()),
    url('^post/(?P<post_id>\d+)/$', PostView.as_view()),
    url('^post/(?P<post_id>\d+)/comments/$', PostCommentsView.as_view()),
    url('^comment/(?P<comment_id>\d+)/$', CommentView.as_view()),
]
