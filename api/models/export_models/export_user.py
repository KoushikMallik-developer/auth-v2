import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from api.models.export_models.export_delivery_address import (
    ExportDeliveryAddressList,
    ExportDeliveryAddress,
)


class ExportECOMUser(BaseModel):
    id: UUID
    username: str
    email: str
    fname: str
    lname: str
    dob: Optional[datetime.datetime]
    phone: Optional[str]
    image: Optional[str]
    is_active: bool
    account_type: str
    delivery_address_list: Optional[ExportDeliveryAddressList] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __init__(self, with_address: bool = False, **kwargs):
        if kwargs.get("image"):
            if not isinstance(kwargs.get("image"), str):
                kwargs["image"] = kwargs.get("image").url
            else:
                kwargs["image"] = None

        from api.models.delivery_address import DeliveryAddress

        if with_address:
            address_list = DeliveryAddress.objects.filter(user__id=kwargs.get("id"))
            address_list = ExportDeliveryAddressList(
                address_list=[
                    ExportDeliveryAddress(**address.model_to_dict())
                    for address in address_list
                ]
            )
            kwargs["delivery_address_list"] = address_list
        super().__init__(**kwargs)


class ExportECOMUserList(BaseModel):
    user_list: typing.List[ExportECOMUser]
