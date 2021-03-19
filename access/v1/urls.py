from django.urls import path

from post.v1.views import PostViewSet

app_name = "post"

post_list = PostViewSet.as_view({"get": "list", "post": "create"})
post_detail = PostViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)


urlpatterns = [
    path("post/", post_list, name="post-list"),
    path("post/<uuid:pk>/", post_detail, name="post-detail"),
]
