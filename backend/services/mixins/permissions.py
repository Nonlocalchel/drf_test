class SelectPermissionByActionMixin:
    """Allow to set rights for each action separately"""
    permission_classes_by_action = None

    def get_permissions(self):
        """Returns rights depending on the action"""
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
