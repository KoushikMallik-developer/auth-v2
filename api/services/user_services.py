from typing import Optional
from djongo.database import DatabaseError
from api.auth_exceptions.user_exceptions import EmailNotSentError
from api.models.export_models.export_user import ExportECOMUser, ExportECOMUserList
from api.models.user import ECOMUser
from api.serializers.ecom_user_serializer import ECOMUserSerializer
from api.services.definitions import (
    DEFAULT_VERIFICATION_MESSAGE,
)
from api.services.otp_services.otp_services import OTPServices


class UserServices:
    @staticmethod
    def get_all_users_service() -> Optional[ExportECOMUserList]:
        try:
            users = ECOMUser.objects.all()
        except Exception:
            raise DatabaseError()
        if users:
            all_user_details = []
            for user in users:
                user_export_details = ExportECOMUser(**user.model_to_dict())
                all_user_details.append(user_export_details)
            all_user_details = ExportECOMUserList(user_list=all_user_details)
            return all_user_details
        else:
            return None

    @staticmethod
    def create_new_user_service(data: dict) -> dict:
        user: ExportECOMUser = ECOMUserSerializer().create(data=data)
        if user:
            response = OTPServices().send_otp_to_user(user.email)
            if response == "OK":
                return {"message": DEFAULT_VERIFICATION_MESSAGE, "error": None}
            else:
                raise EmailNotSentError()
