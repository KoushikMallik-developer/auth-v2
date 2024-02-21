from api.models.export_types.export_user import ExportECOMUserList
from api.models.response_data_types.response_data import ResponseData


class AllUsersResponseData(ResponseData):
    data: ExportECOMUserList
