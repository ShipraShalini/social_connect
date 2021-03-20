from access.constants import STATUS_APPROVED
from access.models import AccessRequest
from access.utils import get_last_valid_access_req_date


class AdminPermissionHandler:
    def get_approved_access_req(self, admin, user):
        return AccessRequest.objects.filter(
            admin=admin,
            user=user,
            status=STATUS_APPROVED,
            created_at__gte=get_last_valid_access_req_date(),
        ).first()

    def is_authorised(self, access_req):
        return bool(access_req)
