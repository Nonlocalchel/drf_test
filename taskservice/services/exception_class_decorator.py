from django.core.exceptions import PermissionDenied


def exc_decorator(message):
    """
    Декоратор для методов классов permission
    При возврате False генерирует PermissionDenied(message) c указаным message
    """

    def _actual_decorator(func_test):
        def _wrapper(*args):
            test_var = func_test(*args)
            if not test_var:
                raise PermissionDenied(message)

            return True

        return _wrapper

    return _actual_decorator


def raise_permission_denied(decorate_methods: list[any]):
    """
    Декоратор для навешивния на методы классов permissions декоратора exc_decorator
    (Не работаeт для классов у которых во View permission_classes = [~IsExamplePermission] указан операнд ~)
    """
    def _actual_decorator(cls: type) -> type:
        class MyCls:
            def __init__(self, *args, **kwargs):
                self._obj = cls(*args, **kwargs)
                super().__init__(*args, **kwargs)

            def __getattribute__(self, item):
                try:
                    obj_attr = super().__getattribute__(item)
                except AttributeError:
                    pass
                else:
                    return obj_attr

                attr = self._obj.__getattribute__(item)
                if isinstance(attr, type(self.__init__)) and item in decorate_methods:
                    message = self._obj.message
                    result_function = exc_decorator(message)(attr)
                    return result_function

                else:
                    return attr

        return MyCls

    return _actual_decorator


