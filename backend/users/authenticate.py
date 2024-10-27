from services.JWTAuthenticationWithCustomUserGet import JWTAuthenticationWithCustomUserGet, AuthUser, \
    api_settings

from users.utils import get_auth_users_fields


class Authenticate(JWTAuthenticationWithCustomUserGet):

    def get_user_orm_fetch(self, user_id, payload) -> AuthUser:
        user_type = payload['type']
        fields = get_auth_users_fields(user_type)

        user_manager = self.user_model.objects
        user_fetch = user_manager.select_related(user_type).only(*fields)
        user = user_fetch.get(**{api_settings.USER_ID_FIELD: user_id})
        return user
