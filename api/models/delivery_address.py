from django.db import models

from api.models.base_address import ECOMBaseAddress
from api.models.definitions import ADDRESS_TYPE_CHOICES
from api.models.user import ECOMUser


class DeliveryAddress(ECOMBaseAddress):
    user = models.ForeignKey(ECOMUser, on_delete=models.CASCADE)
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default="Home",
    )
    is_default = models.BooleanField(default=False)
    delivery_to_phone = models.CharField(max_length=255)
    delivery_to_person_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
