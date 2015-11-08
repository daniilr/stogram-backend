from django.conf.urls import include, url
from .views_api import *
from . import api_urls

urlpatterns = [
    url('^api/', include(api_urls)),
    url('^auth/', include(api_urls)),
    url('^$', "photos.views.landing", name="landing"),
    url('^auth/$', "photos.views.auth", name="auth"),
    url('^submit/$', "photos.views.submit_index", name="submit_index")
]
