from django.db import models

from api.models.base_models.base_model import ECOMBaseModel
from api.models.user_models.user import ECOMUser


class ECOMSellerDetails(ECOMBaseModel):
    seller = models.ForeignKey(ECOMUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name
