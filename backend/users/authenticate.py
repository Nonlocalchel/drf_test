from services.mixins.JWTAuthenticationWithCustomUserGet import JWTAuthenticationWithCustomUserGet, AuthUser, \
    api_settings

from users.utils import get_all_user_types, get_auth_users_fields


class Authenticate(JWTAuthenticationWithCustomUserGet):

    def get_user_orm_fetch(self, user_id) -> AuthUser:
        types = get_all_user_types()
        fields = get_auth_users_fields(types)

        user_manager = self.user_model.objects
        user_fetch = user_manager.select_related(*types).only(*fields)
        user = user_fetch.get(**{api_settings.USER_ID_FIELD: user_id})
        return user
