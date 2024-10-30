from services.JWTAuthenticationWithCustomUserGet import JWTAuthenticationWithCustomUserGet, AuthUser, \
    api_settings
from users.utils.auth_utils import get_auth_users_fields


class Authenticate(JWTAuthenticationWithCustomUserGet):
    """Task service authenticate class(to extend get_user_orm_fetch method)"""

    def get_user_orm_fetch(self, user_id, payload) -> AuthUser:
        """Override method for optimize(get additional fields to orm fetch depending on request)"""
        user_type = []
        fields = []

        path_elements = self.request_path[1:-1].split('/')
        if 'tasks' in path_elements:
            user_type = [payload['type']]
            fields = get_auth_users_fields(user_type)

        elif str(user_id) == path_elements[-1]:
            user_type = [payload['type']]

        user_manager = self.user_model.objects
        user_fetch = user_manager.select_related(*user_type).only(*fields)
        user = user_fetch.get(**{api_settings.USER_ID_FIELD: user_id})
        return user
