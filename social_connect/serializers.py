from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """DRF Serializer for User model"""

    class Meta:
        model = User
        exclude = ["password"]


class MinimalUserSerializer(ModelSerializer):
    """DRF Serializer for User model when only a few public fields are needed."""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_active"]
