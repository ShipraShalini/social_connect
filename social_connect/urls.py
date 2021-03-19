"""social_connect URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

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
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swaggerui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # Verion 1 URLs
    path(
        "v1/",
        include(
            [
                # Auth URLs
                *auth_urls,
                path("", include("post.v1.urls")),
                path("access_req/", include("access.v1.urls")),
            ]
        ),
    ),
    # Schema URLs
    *schema_urls,
]
