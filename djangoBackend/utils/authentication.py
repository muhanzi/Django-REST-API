# import jwt
from djangoBackend.user_module.serializers import TokenSerializer
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class Object(object):
    pass


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):

        authorization_header = request.headers.get('Authorization')
        details = Object()
        details.is_authenticated = False

        if not authorization_header:
            raise exceptions.AuthenticationFailed("An Authorization token is required")
            # TODO: verify token

        access_token = authorization_header.split(' ')[1]
        token_name = authorization_header.split(' ')[0]  # token prefix is "Token"

        try:
            tokens = Token.objects.filter(key=access_token)
            token = [TokenSerializer(
                    tokenInstance).data for tokenInstance in tokens][0]
            details.is_authenticated = True
            details.userId = token["user"]
        except Exception as ex:
            print("=== error token === "+str(ex))
            details.is_authenticated = False

        if not details.is_authenticated:
            raise exceptions.AuthenticationFailed(
                "Invalid authorization token")

        return (details, None)
