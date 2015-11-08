from photos.models import PhotoUser
from django.contrib.auth.models import User
import vk
import vk.exceptions
import uuid
import urllib.request
import requests
from django.conf import settings
import os

class VkBackend(object):
    def authenticate(self, token=None):
        r = requests.get("https://oauth.vk.com/access_token", {
            "client_id": "5136311",
            "client_secret": "PstbepOKAA4mqW0AF4Ok",
            "redirect_uri":  settings.OAUTH_SITE_URL + "auth/",
            "code": token
        })
        data = r.json()
        vk_key = data['access_token']
        email = data['email']
        vk_id = data['user_id']
        try:
            session = vk.Session(access_token=vk_key)
            api = vk.API(session)
            profile = api.users.get(fields="first_name,photo_200_orig,last_name,photo_100")[0]
        except vk.exceptions.VkAPIError:
            return None
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
        if not user.photouser.avatar:
            filepattern = "u%i.jpg" % vk_id
            urllib.request.urlretrieve(
                profile['photo_200_orig'],
                os.path.join(settings.MEDIA_ROOT, "vkava", filepattern)
            )
            urllib.request.urlretrieve(
                profile['photo_100'],
                os.path.join(settings.MEDIA_ROOT, "vkava", "thumb", filepattern)
            )
            user.photouser.avatar = os.path.join("vkava", filepattern)
            user.photouser.thumb = os.path.join("vkava", "thumb", filepattern)
            user.photouser.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None