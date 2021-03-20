import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    DateTimeField,
    ForeignKey,
    TextField,
    UUIDField,
)

from access.constants import (
    ACCESS_REQUEST_STATUS_CHOICES,
    STATUS_EXPIRED,
    STATUS_PENDING,
)
from access.utils import get_last_valid_access_req_date


class AccessRequest(models.Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = ForeignKey(User, on_delete=PROTECT, related_name="admin_requests")
    superadmin = ForeignKey(
        User,
        on_delete=PROTECT,
        related_name="superadmin_requests",
        null=True,
        blank=True,
    )
    user = ForeignKey(User, on_delete=CASCADE)
    request_reason = TextField(null=True, blank=True)
    decision_reason = TextField(null=True, blank=True)
    status = CharField(
        max_length=10, choices=ACCESS_REQUEST_STATUS_CHOICES, default="pending"
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(null=True, blank=True)
    used_at = DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def is_expired(self):
        # Todo: Run a periodic task to mark the request expired.
        return self.status == STATUS_EXPIRED or (
            self.status == STATUS_PENDING
            and self.created_at >= get_last_valid_access_req_date()
        )
