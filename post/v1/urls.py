from django.urls import path

from post.v1.views import AdminPostViewSet, PostViewSet

app_name = "post"

post_list = PostViewSet.as_view({"get": "list", "post": "create"})
post_detail = PostViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
admin_post_list = AdminPostViewSet.as_view({"get": "list", "post": "create"})
admin_post_detail = AdminPostViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)


urlpatterns = [
    path("post/", post_list, name="post-list"),
    path("post/<uuid:pk>/", post_detail, name="post-detail"),
    path("admin/post/", admin_post_list, name="admin-post-list"),
    path("admin/post/<uuid:pk>/", admin_post_detail, name="admin-post-detail"),
]
