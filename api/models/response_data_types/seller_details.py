from typing import Optional

from api.models.export_types.export_seller import ExportECOMSeller
from api.models.response_data_types.response_data import ResponseData


class SellerDetailsResponseData(ResponseData):
    data: Optional[ExportECOMSeller]
