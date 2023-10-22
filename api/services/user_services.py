import logging

from django.forms import model_to_dict

from api.models.export_models.export_user import ExportECOMUser, ExportECOMUserList
from api.models.user import ECOMUser
from api.models.validation_result import ValidationResult
from api.services.encryption_service import EncryptionServices
from api.services.helpers import (
    validate_email,
    validate_name,
    validate_username,
    validate_password,
)
from api.services.token_generator import TokenGenerator


class UserServices:
    @staticmethod
    def get_all_users_service() -> ExportECOMUserList:
        try:
            users = ECOMUser.objects.all()
            all_user_details = []
            for user in users:
                user_export_details = ExportECOMUser(**model_to_dict(user))
                all_user_details.append(user_export_details)
            all_user_details = ExportECOMUserList(user_list=all_user_details)
            return all_user_details
        except Exception:
            logging.error("Database connection error")
            raise Exception("Database connection error")

    def create_new_user_service(self, data: dict) -> dict:
        is_validated_email = False
        is_validated_name = False
        is_validated_username = False
        is_validated_password = False

        email = data.get("email")
        fname = data.get("fname")
        lname = data.get("lname")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        # Email Validation
        if email and isinstance(email, str):
            validation_result_email: ValidationResult = validate_email(email)
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                return {
                    "token": None,
                    "error": validation_result_email.error
                    if validation_result_email.error
                    else "Email Validation Failed",
                }

        # Name and Username Validation
        if (
            fname
            and lname
            and username
            and isinstance(fname, str)
            and isinstance(lname, str)
            and isinstance(username, str)
        ):
            validation_result_name: ValidationResult = validate_name(fname + lname)
            is_validated_name = validation_result_name.is_validated
            if not is_validated_name:
                return {
                    "token": None,
                    "error": validation_result_name.error
                    if validation_result_name.error
                    else "Name Validation Failed",
                }
            validation_result_username: ValidationResult = validate_username(username)
            is_validated_username = validation_result_username.is_validated
            if not is_validated_username:
                return {
                    "token": None,
                    "error": validation_result_username.error
                    if validation_result_username.error
                    else "Username Validation Failed",
                }
        # Password Validation
        if (
            password1
            and password2
            and isinstance(password1, str)
            and isinstance(password2, str)
        ):
            validation_result_password: ValidationResult = validate_password(
                password1, password2
            )
            is_validated_password = validation_result_password.is_validated
            if not is_validated_password:
                return {
                    "token": None,
                    "error": validation_result_password.error
                    if validation_result_password.error
                    else "Password Validation Failed",
                }

        if (
            is_validated_email
            and is_validated_password
            and is_validated_username
            and is_validated_name
        ):
            # Creating ECOMUser Object
            user = ECOMUser(
                email=email,
                username=username,
                fname=fname,
                lname=lname,
                password=EncryptionServices().encrypt(password1),
            )
            try:
                user.save()
            except Exception:
                return {"token": None, "error": "Could not save the user"}
            export_user = ExportECOMUser(**model_to_dict(user))
            token = TokenGenerator().get_tokens_for_user(export_user)
            return {"token": token, "error": None}
