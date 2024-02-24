from typing import Optional
from api.models.export_types.export_user import ExportECOMUser
from api.models.response_data_types.response_data import ResponseData


class UserDetailsResponseData(ResponseData):
    data: Optional[ExportECOMUser]
