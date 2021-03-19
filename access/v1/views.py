from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from access.access_request_handler import AccessRequestHandler
from social_connect.permissions import IsSuperAdminUser


class AdminAccessRequestView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        admin = request.user
        data = request.data
        req = AccessRequestHandler().create(admin, data)
        return JsonResponse(req)

    def get(self, request, *args, **kwargs):
        data = AccessRequestHandler().get_request_list({"admin_id": request.user})
        return JsonResponse(data)


class SuperAdminAccessRequestListView(APIView):
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def get(self, request, *args, **kwargs):
        data = AccessRequestHandler().get_request_list({"superadmin_id": request.user})
        return JsonResponse(data)


class SuperAdminAccessRequestDecisionView(APIView):
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def patch(self, request, access_req_id, *args, **kwargs):
        superadmin = request.user
        data = request.data
        req = AccessRequestHandler().take_decision(access_req_id, superadmin, data)
        return JsonResponse(req)
