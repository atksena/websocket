import traceback
from urllib.parse import parse_qs
import jwt
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework.settings import api_settings
from rest_framework import exceptions

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def compile_request(self, scope, token):
        _request = HttpRequest()
        _request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        _request.method = scope.get('method', None)
        _request.path = scope['path']
        print(token)
        print(_request.headers)

        return _request

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope["query_string"].decode())
        token_param = query_params.get('token')
        token = token_param[0] if len(token_param) else None
        if not token:
            scope['user'] = AnonymousUser()
            return await self.inner(scope, receive, send)
        try:
            _request = self.compile_request(scope, token)
            user, _ = await self.get_user(_request)
            if user and user.is_authenticated:
                scope['user'] = user
        except (jwt.InvalidTokenError, IndexError, KeyError, exceptions.AuthenticationFailed):
            traceback.print_exc()
            pass

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, _request):
        for authentication_class in api_settings.DEFAULT_AUTHENTICATION_CLASSES:
            _user, _ = authentication_class().authenticate(_request)
            if _user:
                return _user, _

        return None, None
