from rest_framework.serializers import ModelSerializer

from access.models import AccessRequest
from social_connect.serializers import MinimalUserSerializer


class AccessRequestSerializer(ModelSerializer):
    raised_by = MinimalUserSerializer()
    super_admin = MinimalUserSerializer()
    user = MinimalUserSerializer()

    class Meta:
        model = AccessRequest
        fields = "__all__"
