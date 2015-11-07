from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class VkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get('token')

        if not token:
            return None

        try:
            user = User.objects.get(photouser__auth_token=token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Your token is expied. Idi nahuy suka')

        return (user, None)
