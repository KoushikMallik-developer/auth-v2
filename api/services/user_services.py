import logging
from typing import Optional

from rest_framework import serializers

from api.models.export_models.export_user import ExportECOMUser, ExportECOMUserList
from api.models.user import ECOMUser
from api.serializers.ecom_user_serializer import ECOMUserSerializer
from api.services.definitions import default_verification_message, default_verification_message_email_failed
from api.services.otp_services.otp_services import OTPServices
from api.services.token_generator import TokenGenerator


class UserServices:
    @staticmethod
    def get_all_users_service() -> Optional[ExportECOMUserList]:
        try:
            users = ECOMUser.objects.all()
            all_user_details = []
            for user in users:
                user_export_details = ExportECOMUser(**user.model_to_dict())
                all_user_details.append(user_export_details)
            all_user_details = ExportECOMUserList(user_list=all_user_details)
            return all_user_details
        except Exception:
            logging.error("Database connection error")
            return None

    @staticmethod
    def create_new_user_service(data: dict) -> dict:
        message = None
        try:
            serializer = ECOMUserSerializer()
            user: ExportECOMUser = serializer.create(data=data)
            if user:
                # token = TokenGenerator().get_tokens_for_user(user)
                response = OTPServices().send_otp_to_user(user.email)
                if response == "OK":
                    message = default_verification_message
                else:
                    message = default_verification_message_email_failed

        except serializers.ValidationError as e:
            return {"message": message, "error": e.detail}
        return {"message": message, "error": None}
