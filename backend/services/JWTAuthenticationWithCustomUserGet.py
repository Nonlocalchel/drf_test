from typing import Optional, Tuple

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password


class JWTAuthenticationWithCustomUserGet(JWTAuthentication):
    request_path = None

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        self.request_path = request.path
        return super().authenticate(request)

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            payload = validated_token.payload
            user_id = payload.pop(api_settings.USER_ID_CLAIM)
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = self.get_user_orm_fetch(user_id, payload)
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(
                    api_settings.REVOKE_TOKEN_CLAIM
            ) != get_md5_hash_password(user.password):
                raise AuthenticationFailed(
                    _("The user's password has been changed."), code="password_changed"
                )

        return user

    def get_user_orm_fetch(self, user_id, payload) -> AuthUser:
        return self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})

