from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from access.access_request_handler import AccessRequestHandler
from access.constants import STATUS_APPROVED, STATUS_IN_USE, STATUS_USED
from social_connect.custom_views import CustomModelViewSet


class AbstractAdminOverrideViewSet(CustomModelViewSet):
    """
    A CRUD viewset for the admins.

    Checks for a valid approved access request for the request to be authorized.
    SuperAdmins also need a valid approved access request for record.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def dispatch(self, request, *args, **kwargs):
        """
        Adds attribute `access_req` to request before checking permissions.
        `access_req` attribute can be `None`.

        Updates AccessRequest status at different stages of request processing along
        with regular dispatch functions.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
                response = self.call_handler(request, handler, *args, **kwargs)
            else:
                handler = self.http_method_not_allowed
                response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def call_handler(self, request, handler, *args, **kwargs):
        # Adding attribute `access_req` to request.
        self.get_approved_access_req(request)
        # Adding `updated_by` to the request data.
        request.data["updated_by"] = request.user.id
        # Keeping this out of the atomic block as
        # it needs to be set before starting the transaction.
        self.access_req_handler.mark_status(request.access_req, STATUS_IN_USE)
        try:
            with transaction.atomic():
                response = handler(request, *args, **kwargs)
                # Reverting the status back to approved as the process failed.
                self.access_req_handler.mark_status(request.access_req, STATUS_USED)
        except Exception:
            self.access_req_handler.mark_status(request.access_req, STATUS_APPROVED)
            raise
        return response

    def get_approved_access_req(self, request):
        """
        Check if the admin has proper access.
        If yes, attach the access_req to the request.
        """
        admin = request.user
        user_id = request.data.get("user_id")
        if not user_id:
            raise ValidationError("`user_id` is required.")
        self.access_req_handler = AccessRequestHandler()
        access_req = self.access_req_handler.get_oldest_valid_approved_access_req(
            admin, user_id
        )
        if not access_req:
            raise PermissionDenied("No valid approved access request found.")
        request.access_req = access_req
