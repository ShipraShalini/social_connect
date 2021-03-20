import json
import logging
from datetime import datetime
from urllib.parse import parse_qs

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from social_connect.constants import (
    CONTENT_TYPE_METHOD_MAP,
    HTTP_HEADER_LIST,
    MASKED_DATA,
)
from social_connect.exception_handler import ExceptionHandler
from social_connect.utils import get_ip, get_user_agent, is_api_request

logger = logging.getLogger("access_log")


class LogMiddleware:
    def __init__(self, get_response):
        """Initialize."""
        self.get_response = get_response

    def _get_urlencoded_data(self, request_body, **kwargs):
        """Return the URL Encoded data from request body."""
        return parse_qs(request_body)

    def _get_json_data(self, request_body, **kwargs):
        """Return JSON data from the request body."""
        return json.loads(request_body)

    def _decode_unicode_data(self, request_body):
        """Decoding unicode data first else the following statement may fail."""
        if isinstance(request_body, bytes):
            try:
                return request_body.decode("utf-8")
            except UnicodeDecodeError:
                pass

    def get_request_data(self, request, request_body):
        """
        Process request data.
        Handling only JSON data, can be extended to get other formats.
        """
        request_body = self._decode_unicode_data(request_body)
        method_name = CONTENT_TYPE_METHOD_MAP.get(request.content_type, "")
        method = getattr(self, method_name, None)
        try:
            return (
                method(request=request, request_body=request_body) if method else None
            )
        except Exception:  # noqa
            return None

    def get_headers(self, request):
        """Return the headers from the request."""
        headers = {}
        for header, value in request.META.items():
            if header.startswith("HTTP_") or header in HTTP_HEADER_LIST:
                headers[header] = value
        return headers

    def mask_auth_token(self, response_data):
        """
        Mask token if present in response.

        This can be extended to mask tokens sent for
        reset password, email verification etc.
        """
        if not isinstance(response_data, dict):
            return
        data = response_data
        if "refresh" in response_data:
            data["refresh"] = self._mask_token(data["refresh"])
        elif "access" in response_data:
            data["refresh"] = self._mask_token(data["access"])

    def _mask_token(self, token):
        """
        Mask the bearer token.

        This is done so that one has some idea about the token format.
        """
        return f"{token[:15]}{MASKED_DATA}{token[-10:]}"

    def mask_data(self, request_data, response_data, headers):
        """Mask sensitive data before logging."""
        if (
            request_data
            and isinstance(request_data, dict)
            and "password" in request_data
        ):
            request_data["password"] = MASKED_DATA

        if response_data:
            self.mask_auth_token(response_data)

        if headers and "HTTP_AUTHORIZATION" in headers:
            auth_header = headers["HTTP_AUTHORIZATION"]
            headers["HTTP_AUTHORIZATION"] = self._mask_token(auth_header)

    def get_response_data(self, request, response):
        error_data = getattr(request, "error_data", None)
        if error_data:
            return error_data
        try:
            return json.loads(response.content.decode("utf8"))
        except json.decoder.JSONDecodeError:
            return None

    def __call__(self, request):
        if not is_api_request(request):
            return self.get_response(request)
        request_body = request.body
        requested_at = datetime.utcnow()
        response = self.get_response(request)
        path = request.get_full_path()
        method = request.method
        status_code = response.status_code
        response_data = self.get_response_data(request, response)
        request_body = self.get_request_data(request, request_body)
        response_time = datetime.utcnow() - requested_at
        response_time = round(response_time.total_seconds() * 1000)

        response_data = json.loads(json.dumps(response_data, cls=DjangoJSONEncoder))

        user = request.user if request.user.is_authenticated else None

        headers = self.get_headers(request)
        self.mask_data(request_body, response_data, headers)
        raw_agent, pretty_agent = get_user_agent(headers)

        try:
            log_data = json.dumps(
                {
                    "user": user.username if user else None,
                    "path": path,
                    "method": method,
                    "request_data": request_body,
                    "requested_at": requested_at,
                    "response_time": int(response_time),
                    "status_code": status_code,
                    "response_data": response_data,
                    "ip": get_ip(headers),
                    "raw_user_agent": raw_agent,
                    "user_agent": pretty_agent,
                    "headers": headers,
                },
                cls=DjangoJSONEncoder,
            )
            logger.info(log_data)
        except Exception as e:  # noqa
            logger.error(e)
        if getattr(request, "error_data", None):
            return JsonResponse(request.error_data, status=response.status_code)
        return response


class JSONExceptionMiddleWare:
    def __init__(self, get_response):
        """Initialize."""
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not is_api_request(request):
            return
        error_data = ExceptionHandler().handle_exception(request, exception)
        request.error_data = error_data
