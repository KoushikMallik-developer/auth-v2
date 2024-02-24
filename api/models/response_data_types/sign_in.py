from typing import Optional

from api.models.response_data_types.response_data import ResponseData


class SignInResponseData(ResponseData):
    token: Optional[str]
