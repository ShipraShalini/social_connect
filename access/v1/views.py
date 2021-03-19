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
        data = AccessRequestHandler().get_request_list({"raised_by_id": request.user})
        return JsonResponse(data)


class SuperAdminAccessRequestView(APIView):
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def get(self, request, *args, **kwargs):
        data = AccessRequestHandler().get_request_list({"superadmin_id": request.user})
        return JsonResponse(data)

    def patch(self, request, uuid, *args, **kwargs):
        superadmin = request.user
        data = request.data
        req = AccessRequestHandler().create(superadmin, data)
        return JsonResponse(req)
