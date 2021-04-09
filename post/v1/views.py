from rest_framework.permissions import IsAuthenticated

from post.serializers import PostSerializer
from social_connect.admin_override_views import AbstractAdminOverrideViewSet
from social_connect.custom_views import CustomModelViewSet


class PostViewSet(CustomModelViewSet):
    """A simple ViewSet for Post CRUD"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.posts.all()

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        request.data["created_by"] = request.user
        return super().create(request, *args, **kwargs)


class AdminPostViewSet(AbstractAdminOverrideViewSet):
    """
    A Post CRUD for the admins.
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        return self.request.access_req.user.posts.all()

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.access_req.user_id
        request.data["created_by"] = request.access_req.admin_id
        return super().create(request, *args, **kwargs)
