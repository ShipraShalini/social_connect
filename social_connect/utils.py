from user_agents import parse


def get_user_agent(headers):
    """Get user agent from the request."""
    raw_agent = headers.get("HTTP_USER_AGENT") or ""
    pretty_agent = str(parse(raw_agent))
    return raw_agent, pretty_agent


def get_ip(headers):
    return headers.get("HTTP_X_FORWARDED_FOR") or headers.get("REMOTE_ADDR")


def is_api_request(request):
    return "api" in request.path
