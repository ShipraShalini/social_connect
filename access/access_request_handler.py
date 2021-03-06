from rest_framework.exceptions import ValidationError

from access.constants import (
    STATUS_APPROVED,
    STATUS_DECLINED,
    STATUS_EXPIRED,
    STATUS_IN_USE,
    STATUS_PENDING,
    STATUS_USED,
)
from access.models import AccessRequest
from access.serializers import AccessRequestSerializer
from access.utils import get_last_valid_access_req_date


class AccessRequestHandler:
    """Class for handling AccessRequests."""

    def create(self, admin, data):
        """Create AccessRequest."""
        # Discarding all other keys provided in the data as
        # only the following fields should be updated.
        data = {
            "admin": admin,
            "request_reason": data.get("request_reason"),
            "user_id": data["user_id"],
        }
        req = AccessRequestSerializer().create(data)
        return AccessRequestSerializer(req).data

    def get_request_list(self, query):
        """Return the list of all access requests for an admin or a superadmin."""
        data = {
            STATUS_PENDING: [],
            STATUS_APPROVED: [],
            STATUS_DECLINED: [],
            STATUS_USED: [],
            STATUS_IN_USE: [],
        }
        # Get only valid requests.
        last_valid_date = get_last_valid_access_req_date()
        requests = AccessRequest.objects.filter(
            **query, created_at__gte=last_valid_date
        )
        if "superadmin_id" in query:
            requests |= AccessRequest.objects.filter(
                status=STATUS_PENDING, created_at__gte=last_valid_date
            )
        requests = AccessRequestSerializer(requests, many=True).data
        for req in requests:
            data[req["status"]].append(req)
        return data

    def take_decision(self, access_req_id, superadmin, data):
        """Approve or Decline an AccessRequest."""
        status = data.get("status")
        if status not in [STATUS_APPROVED, STATUS_DECLINED]:
            raise ValidationError("Status is missing or is invalid.")
        # Discarding all other keys provided in the data as
        # only the following fields should be updated.
        data = {
            "superadmin": superadmin,
            "decision_reason": data.get("decision_reason"),
            "status": status,
        }
        AccessRequest.objects.filter(uuid=access_req_id).update(**data)
        req = AccessRequest.objects.get(uuid=access_req_id)
        return AccessRequestSerializer(req).data

    def mark_status(self, access_req, status):
        access_req.status = status
        access_req.save()

    def mark_expired(self):
        """Mark a request expired."""
        # TODO: Run a periodic task to mark requests expired.
        last_valid_date = get_last_valid_access_req_date()
        AccessRequest.objects.filter(
            status=STATUS_PENDING, created_at__lt=last_valid_date
        ).update(status=STATUS_EXPIRED)

    def get_oldest_valid_approved_access_req(self, admin, user_id):
        """Return the oldest valid aprroved access req as it will be used first."""
        return (
            AccessRequest.objects.select_related("user")
            .filter(
                admin=admin,
                user_id=user_id,
                status=STATUS_APPROVED,
                created_at__gte=get_last_valid_access_req_date(),
            )
            .last()
        )
