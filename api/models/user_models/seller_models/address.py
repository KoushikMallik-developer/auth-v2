from django.db import models

from api.models.base_models.base_address import ECOMBaseAddress
from api.models.user_models.user import ECOMUser


class SellerAddress(ECOMBaseAddress):
    seller = models.ForeignKey(ECOMUser, on_delete=models.CASCADE)
