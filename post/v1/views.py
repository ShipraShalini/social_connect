from django.db import transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from access.access_request_handler import AccessRequestHandler
from access.constants import STATUS_APPROVED, STATUS_IN_USE, STATUS_USED
from access.permissions import IsAuthorised
from post.serializers import PostSerializer
from social_connect.custom_views import CustomModelViewSet


class PostViewSet(CustomModelViewSet):
    """A simple ViewSet for Post CRUD"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.posts.all()

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user
        request.data["created_by"] = request.user
        return super().create(request, *args, **kwargs)


class AdminPostViewSet(CustomModelViewSet):
    """
    A Post CRUD for the admins.

    Checks for a valid approved access request for the request to be authorized.
    Superadmins also need a valid approved access request for record.

    Assuming that the calls by admin will used not very often,
    overriding the view methods instead of adding a middleware
    which will be called for all requests.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, IsAuthorised]

    def initial(self, request, *args, **kwargs):
        """
        Adds attribute `access_req` to request before checking permissions.
        `access_req` attribute can be `None`.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        # Adding attribute `access_req` to request.
        self.get_approved_access_req(request)
        self.check_permissions(request)
        self.check_throttles(request)

    def dispatch(self, request, *args, **kwargs):
        """
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
            else:
                handler = self.http_method_not_allowed

            # Adding `updated_by` to the request data.
            request.data["updated_by"] = request.user
            # Keeping this out of the atomic block as
            # it needs to be set before starting the transaction.
            self.access_req_handler.mark_status(request.access_req, STATUS_IN_USE)
            with transaction.atomic():
                response = handler(request, *args, **kwargs)
                self.access_req_handler.mark_status(request.access_req, STATUS_USED)

        except Exception as exc:
            response = self.handle_exception(exc)
            # Reverting the status back to approved as the process failed.
            self.access_req_handler.mark_status(request.access_req, STATUS_APPROVED)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def get_approved_access_req(self, request):
        admin = request.user
        user_id = request.data.get("user_id")
        self.access_req_handler = AccessRequestHandler()
        access_req = self.access_req_handler.get_oldest_valid_approved_access_req(
            admin, user_id
        )
        request.access_req = access_req

    def get_queryset(self):
        return self.request.access_req.user.posts.all()

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.access_req.user
        request.data["created_by"] = request.access_req.admin
        return super().create(request, *args, **kwargs)
