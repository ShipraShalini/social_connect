import uuid

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
    UUIDField,
)


class Post(Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(
        User, related_name="posts", on_delete=CASCADE, null=False, blank=False
    )
    message = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
