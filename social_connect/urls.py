"""social_connect URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from social_connect.api_response import APIResponse

# Overriding default exception handlers for 404 & 403 errors.
handler404 = "social_connect.exception_handler.json_page_not_found"
handler403 = "social_connect.exception_handler.json_permission_denied"


@api_view(("GET",))
def health(request):
    return APIResponse({"status": "healthy"})


auth_urls = [
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

schema_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swaggerui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


v1_urls = [
    # Auth URLs
    *auth_urls,
    path("", include("post.v1.urls")),
    path("access_req/", include("access.v1.urls")),
]
urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # Verion 1 URLs
    path(
        "api/",
        include(
            [
                path("v1/", include(v1_urls)),
            ]
        ),
    ),
    # Schema URLs
    *schema_urls,
    path("", health),
]
