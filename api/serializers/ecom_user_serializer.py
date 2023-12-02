from typing import Optional

from django.forms import model_to_dict
from rest_framework import serializers

from api.models.export_models.export_user import ExportECOMUser
from api.models.user import ECOMUser
from api.models.validation_result import ValidationResult
from api.services.encryption_service import EncryptionServices
from api.services.helpers import (
    validate_email,
    validate_name,
    validate_username,
    validate_password,
)


class ECOMUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECOMUser
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
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
                raise serializers.ValidationError(detail=validation_result_email.error)

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
                raise serializers.ValidationError(detail=validation_result_name.error)
            validation_result_username: ValidationResult = validate_username(username)
            is_validated_username = validation_result_username.is_validated
            if not is_validated_username:
                raise serializers.ValidationError(validation_result_username.error)
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
                raise serializers.ValidationError(validation_result_password.error)

        if (
            is_validated_email
            and is_validated_password
            and is_validated_username
            and is_validated_name
        ):
            return True

    def create(self, data: dict) -> ExportECOMUser:
        email = data.get("email")
        fname = data.get("fname")
        lname = data.get("lname")
        username = data.get("username")
        password1 = data.get("password1")
        if self.validate(data):
            user = ECOMUser(
                email=email,
                username=username,
                fname=fname,
                lname=lname,
                password=EncryptionServices().encrypt(password1),
            )
            user.save()
            return ExportECOMUser(**model_to_dict(user))
