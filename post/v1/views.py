from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from post.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    """A simple ViewSet for Post CRUD"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.posts.all()
