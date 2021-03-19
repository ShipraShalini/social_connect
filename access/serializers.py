from rest_framework.serializers import ModelSerializer

from access.models import AccessRequest
from social_connect.serializers import MinimalUserSerializer


class AccessRequestSerializer(ModelSerializer):
    admin = MinimalUserSerializer()
    superadmin = MinimalUserSerializer()
    user = MinimalUserSerializer()

    class Meta:
        model = AccessRequest
        fields = "__all__"
