from django.urls import path

from access.v1.views import (
    AdminAccessRequestView,
    SuperAdminAccessRequestDecisionView,
    SuperAdminAccessRequestListView,
)

app_name = "access"


urlpatterns = [
    path("admin/", AdminAccessRequestView.as_view(), name="admin-access"),
    path(
        "superadmin/",
        SuperAdminAccessRequestListView.as_view(),
        name="superadmin-list",
    ),
    path(
        "decision/<uuid:access_req_id>",
        SuperAdminAccessRequestDecisionView.as_view(),
        name="superadmin-decision",
    ),
]
