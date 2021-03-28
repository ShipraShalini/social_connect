HTTP_HEADER_LIST = [
    "REMOTE_ADDR",
    "REMOTE_HOST",
    "X_FORWARDED_FOR",
    "TZ",
    "QUERY_STRING",
    "CONTENT_LENGTH",
    "CONTENT_TYPE",
    "LC_CTYPE",
    "SERVER_PROTOCOL",
    "SERVER_SOFTWARE",
]
MASKED_DATA = "XXXXXXXXX"

CONTENT_TYPE_JSON = "application/json"

CONTENT_TYPE_METHOD_MAP = {CONTENT_TYPE_JSON: "_get_json_data"}

CLIENT_ERROR_SET = {
    "AttributeError",
    "IntegrityError",
    "KeyError",
    "ValidationError",
}

BUILTIN_ERROR_MESSAGE = {
    "Http404": "Not found",
    "PermissionDenied": "Permission denied.",
}

MODEL_VIEWSET_METHODNAMES = ["create", "retrieve", "list", "update", "destroy"]

RESPONSE_KEY_DATA = "data"
RESPONSE_KEY_ERROR = "error"
RESPONSE_KEY_IS_SUCCESS = "is_success"
