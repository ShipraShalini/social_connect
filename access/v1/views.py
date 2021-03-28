from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from access.access_request_handler import AccessRequestHandler
from social_connect.api_response import APIResponse
from social_connect.permissions import IsSuperAdminUser


class AdminAccessRequestView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        admin = request.user
        data = request.data
        req = AccessRequestHandler().create(admin, data)
        return APIResponse(req)

    def get(self, request, *args, **kwargs):
        data = AccessRequestHandler().get_request_list({"admin_id": request.user})
        return APIResponse(data)


class SuperAdminAccessRequestListView(APIView):
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def get(self, request, *args, **kwargs):
        data = AccessRequestHandler().get_request_list({"superadmin_id": request.user})
        return APIResponse(data)


class SuperAdminAccessRequestDecisionView(APIView):
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def patch(self, request, access_req_id, *args, **kwargs):
        superadmin = request.user
        data = request.data
        req = AccessRequestHandler().take_decision(access_req_id, superadmin, data)
        return APIResponse(req)
