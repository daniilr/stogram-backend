from django.conf.urls import include, url
from .views import *
from . import api_urls

urlpatterns = [
    url('^', include(api_urls)),
]
