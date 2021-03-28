from rest_framework import status as http_status
from rest_framework.response import Response

from social_connect.constants import (
    CONTENT_TYPE_JSON,
    RESPONSE_KEY_DATA,
    RESPONSE_KEY_ERROR,
    RESPONSE_KEY_IS_SUCCESS,
)


class APIResponse(Response):
    """Custom API Response class."""

    def __init__(
        self,
        data=None,
        status=http_status.HTTP_200_OK,
        is_success=None,
        content_type=CONTENT_TYPE_JSON,
        **kwargs
    ):
        """Initialize API response."""
        is_success = (
            http_status.is_success(status) if is_success is None else is_success
        )

        key = RESPONSE_KEY_DATA if is_success else RESPONSE_KEY_ERROR

        if not data and not isinstance(data, list):
            data = {}

        response_data = {RESPONSE_KEY_IS_SUCCESS: is_success, key: data}
        super().__init__(
            data=response_data, status=status, content_type=content_type, **kwargs
        )
