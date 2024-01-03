import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from api.models.export_types.export_address import ExportAddress
from api.models.user_models.seller_models.address import SellerAddress
from api.models.user_models.seller_models.seller_details import ECOMSellerDetails


class ExportECOMSeller(BaseModel):
    id: Optional[UUID]
    username: str
    email: str
    fname: str
    lname: str
    dob: Optional[datetime.datetime]
    phone: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = None
    account_type: str
    company_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    address: Optional[ExportAddress] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __init__(
        self, with_id: bool = False, additional_details: bool = False, **kwargs
    ):
        if kwargs.get("id"):
            if additional_details:
                details_dict = {}
                if ECOMSellerDetails.objects.filter(
                    seller__id=kwargs.get("id")
                ).exists():
                    details = ECOMSellerDetails.objects.get(seller__id=kwargs.get("id"))
                    details_dict = details.model_to_dict()
                    if SellerAddress.objects.filter(
                        seller__id=kwargs.get("id")
                    ).exists():
                        address = SellerAddress.objects.get(seller__id=kwargs.get("id"))
                        kwargs["address"] = ExportAddress(**address.model_to_dict())
                        if details.updated_at < address.updated_at:
                            details.updated_at = address.updated_at
                            details_dict = details.model_to_dict()
                kwargs.update(details_dict)
            if not with_id:
                kwargs["id"] = None
        super().__init__(**kwargs)
