class SelectPermissionByActionMixin:
    """Миксин permissions для action"""
    permission_classes_by_action = None

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class SelectSerializerByActionMixin:
    serializer_classes_by_action = None

    def get_serializer_class(self):
        serializer_class = self.get_serializer_classes_by_action[self.action]
        return serializer_class

    @property
    def get_serializer_classes_by_action(self):
        return self.serializer_classes_by_action
