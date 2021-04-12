from rest_framework.serializers import ModelSerializer

from post.models import Post


class PostSerializer(ModelSerializer):
    """Serialiser for POST model."""

    class Meta:
        model = Post
        fields = "__all__"
