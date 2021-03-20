import uuid

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
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
    title = CharField(max_length=510)
    message = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by = ForeignKey(
        User, on_delete=PROTECT, null=False, blank=False, related_name="created_posts"
    )
    updated_by = ForeignKey(
        User, on_delete=PROTECT, null=False, blank=False, related_name="updated_posts"
    )

    class Meta:
        ordering = ["-created_at"]
