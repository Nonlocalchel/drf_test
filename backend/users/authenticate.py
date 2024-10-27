from services.JWTAuthenticationWithCustomUserGet import JWTAuthenticationWithCustomUserGet, AuthUser, \
    api_settings

from users.utils import get_auth_users_fields, get_user_types


class Authenticate(JWTAuthenticationWithCustomUserGet):

    def get_user_orm_fetch(self, user_id, payload) -> AuthUser:
        user_type = [payload['type'], ]
        fields = []

        path_elements = self.request_path[1:-1].split('/')
        match path_elements:
            case [*args, 'tasks']:
                fields = get_auth_users_fields(user_type)
            case [*args, 'users', str(user_id)]:
                user_type = [*get_user_types()]
            case [*args, 'users']:
                user_type = []

        user_manager = self.user_model.objects
        user_fetch = user_manager.select_related(*user_type).only(*fields)
        user = user_fetch.get(**{api_settings.USER_ID_FIELD: user_id})
        return user




