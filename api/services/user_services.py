import os
from typing import Optional
from djongo.database import DatabaseError
from dotenv import load_dotenv

from api.auth_exceptions.user_exceptions import EmailNotSentError, UserNotFoundError
from api.models.export_models.export_user import ExportECOMUser, ExportECOMUserList
from api.models.user import ECOMUser
from api.serializers.ecom_user_serializer import ECOMUserSerializer
from api.services.definitions import (
    DEFAULT_VERIFICATION_MESSAGE,
)
from api.services.email_services import EmailServices
from api.services.helpers import validate_user_email
from api.services.otp_services.otp_services import OTPServices
from api.services.token_generator import TokenGenerator


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
                return {
                    "successMessage": DEFAULT_VERIFICATION_MESSAGE,
                    "errorMessage": None,
                }
            else:
                raise EmailNotSentError()

    @staticmethod
    def sign_in_user(data: dict) -> dict:
        email = data.get("email")
        password = data.get("password")
        if email and password:
            response = ECOMUser.authenticate(email=email, password=password)
            return response

    def reset_password(self, email: str) -> dict:
        if validate_user_email(email=email).is_validated:
            reset_url = self.generate_reset_password_url(email=email)
            if (
                EmailServices.send_password_reset_email_by_user_email(
                    user_email=email, reset_url=reset_url
                )
                == "OK"
            ):
                return {
                    "successMessage": "Password reset link sent successfully.",
                    "errorMessage": None,
                }
            else:
                raise EmailNotSentError()
        else:
            raise UserNotFoundError()

    @staticmethod
    def generate_reset_password_url(email: str) -> str:
        user = ECOMUser.objects.get(email=email)
        token = (
            TokenGenerator()
            .get_tokens_for_user(ExportECOMUser(**user.model_to_dict()))
            .get("access")
        )
        load_dotenv()
        FRONTEND_BASE_URL = os.environ.get("FRONTEND_BASE_URL")
        reset_url = f"{FRONTEND_BASE_URL}/password-reset/{token}/"
        return reset_url
