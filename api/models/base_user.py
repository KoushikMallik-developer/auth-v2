import uuid

from django.db import models

from api.models.definitions import ACCOUNT_TYPE_CHOICES


class BaseUser(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, null=False, editable=False
    )
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default="Regular",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
