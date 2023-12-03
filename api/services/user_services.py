import logging

from rest_framework import serializers

from api.models.export_models.export_user import ExportECOMUser, ExportECOMUserList
from api.models.user import ECOMUser
from api.serializers.ecom_user_serializer import ECOMUserSerializer
from api.services.token_generator import TokenGenerator


class UserServices:
    @staticmethod
    def get_all_users_service() -> ExportECOMUserList:
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
            raise Exception("Database connection error")

    @staticmethod
    def create_new_user_service(data: dict) -> dict:
        try:
            serializer = ECOMUserSerializer()
            user: ExportECOMUser = serializer.create(data=data)
            token = TokenGenerator().get_tokens_for_user(user)
        except serializers.ValidationError as e:
            return {"token": None, "error": e.detail}
        return {"token": token, "error": None}
