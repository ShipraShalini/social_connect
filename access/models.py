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


class AccessRequest(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raised_by = ForeignKey(User, on_delete=PROTECT, related_name="admin_requests")
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
    status = CharField(max_length=10, choices=STATUS, default="pending")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
