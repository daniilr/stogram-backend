from django.shortcuts import render, redirect
from django.conf import settings
import requests
import vk
import vk.exceptions
from django.contrib.auth.models import User
import uuid
from .models import *
import urllib
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

def landing(request):
    return render(request, "landing/landning.html", {
        # Все очень плохо
        "vk_auth_url": "https://oauth.vk.com/authorize?client_id=" + settings.VK_APP_ID + " %display=page&"
                       "&scope=wall,friends,email&response_type=code&v=5.40&redirect_uri=" + settings.OAUTH_SITE_URL + "auth/"
    })

def auth(request):
    user = authenticate(token=request.GET.get('code'))
    user.is_active
    request.user = user
    return render(request, "submit/index.html")


def submit_index(request):
    request.session['gasf'] = 1
    return render(request, "submit/index.html")
