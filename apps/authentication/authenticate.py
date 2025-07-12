# pylint: disable=raise-missing-from
from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from rest_framework.request import Request

from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.authentication.services import get_token_service
from pkg.client.client import get_client_info

User = get_user_model()
service = get_token_service()


class JWTAuthentication(BaseJWTAuthentication):

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            service.validate_token(token_str=raw_token.decode(), client_info=get_client_info(request=request))
        except Exception:
            raise InvalidToken()

        return super().authenticate(request=request)
