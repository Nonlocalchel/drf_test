from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import status

from rest_framework.views import exception_handler
from rest_framework.response import Response

def django_error_handler(exc, context):
    """Handle django core's errors."""
    response = exception_handler(exc, context)
    if response is None and isinstance(exc, ValidationError):
        """
        Обработка исключений валидаторов из validators.py
        """
        return Response(status=400, data=exc.message_dict)

    if isinstance(exc, PermissionDenied):
        """
        Обработка исключений которые выкидывают сериализаторы,
        чтобы вывести сообщение message т.к. при (При IsFirstPermission | IsSecondPermission) message, 
        определенные в коде - игнорируются
        """
        return Response(status=status.HTTP_403_FORBIDDEN, data=str(exc))

    return response
