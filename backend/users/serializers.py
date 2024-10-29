from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from .utils.serializer_utils import fix_serializer_fields, get_instance_type, format_repr


# from .utils import fix_serializer_fields, format_repr, get_instance_type


class WorkerSerializer(serializers.ModelSerializer):
    """Serialize nested profile data for worker"""

    class Meta:
        model = Worker
        fields = ['pk', 'exp', 'speciality', 'education']


class CustomerSerializer(serializers.ModelSerializer):
    """Serialize nested profile data for worker"""

    class Meta:
        model = Customer
        fields = ['pk', 'discount', 'legal']


class UserSerializer(WritableNestedModelSerializer):
    """User serializer class"""
    password = serializers.CharField(write_only=True)

    worker = WorkerSerializer(allow_null=True, default=None)

    customer = CustomerSerializer(allow_null=True, default=None)

    class Meta:
        model = User
        fields = (
            'pk',
            'username', 'phone', 'is_staff',
            'type', 'email',
            'first_name', 'last_name', 'is_superuser',
            'worker', 'customer', 'photo',
            'password'
        )

    def get_fields(self):
        """Remove unnecessary professional data fields(for remove unnecessary requests to db)"""
        fields = super().get_fields()
        instance = self.instance
        if instance is None:
            fixed_fields = fix_serializer_fields(instance, fields, data=self.initial_data)
        else:
            fixed_fields = fix_serializer_fields(instance, fields)

        return fixed_fields

    def to_representation(self, instance):
        """Remove unnecessary fields and add professional_data field"""
        representation = super().to_representation(instance)
        user_type = get_instance_type(instance)
        formatted_representation = format_repr(representation, user_type)
        return formatted_representation


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Override class for extend data on payload"""
    @classmethod
    def get_token(cls, user):
        """Add user type field to payload"""
        token = super().get_token(user)
        token['type'] = user.type
        return token
