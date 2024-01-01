from api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserNotVerifiedError,
    UserAuthenticationFailedError,
)
from api.models.user_models.abstract_user import AbstractUser
from api.models.export_types.export_user import ExportECOMUser
from api.services.encryption_services.encryption_service import EncryptionServices
from api.services.token_services.token_generator import TokenGenerator


class ECOMUser(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def authenticate_user(email, password) -> dict:
        user_exists = (
            True if ECOMUser.objects.filter(email=email).count() > 0 else False
        )
        if user_exists:
            user = ECOMUser.objects.get(email=email)
            if user and user.get_is_regular:
                if user.is_active:
                    if EncryptionServices().decrypt(user.password) == password:
                        token = TokenGenerator().get_tokens_for_user(
                            ExportECOMUser(**user.model_to_dict())
                        )
                        return {
                            "token": token,
                            "errorMessage": None,
                        }
                    else:
                        raise UserAuthenticationFailedError()
                else:
                    raise UserNotVerifiedError()
            else:
                raise UserNotFoundError()
        else:
            raise UserNotFoundError()

    @staticmethod
    def authenticate_seller(email, password) -> dict:
        user_exists = (
            True if ECOMUser.objects.filter(email=email).count() > 0 else False
        )
        if user_exists:
            user = ECOMUser.objects.get(email=email)
            if user and user.get_is_seller:
                if user.is_active:
                    if EncryptionServices().decrypt(user.password) == password:
                        token = TokenGenerator().get_tokens_for_user(
                            ExportECOMUser(**user.model_to_dict())
                        )
                        return {
                            "token": token,
                            "errorMessage": None,
                        }
                    else:
                        raise UserAuthenticationFailedError()
                else:
                    raise UserNotVerifiedError()
            else:
                raise UserNotFoundError()
        else:
            raise UserNotFoundError()
