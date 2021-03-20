from datetime import datetime, timedelta

from access.constants import ACCESS_REQUEST_VALID_DAYS


def get_last_valid_access_req_date():
    return datetime.utcnow() - timedelta(days=ACCESS_REQUEST_VALID_DAYS)
