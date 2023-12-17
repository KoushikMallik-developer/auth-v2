from api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserNotVerifiedError,
    UserAuthenticationFailedError,
)
from api.models.abstract_user import AbstractUser
from api.services.encryption_service import EncryptionServices
from api.services.token_generator import TokenGenerator


class ECOMUser(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def authenticate(email, password) -> dict:
        user_exists = (
            True if ECOMUser.objects.filter(email=email).count() > 0 else False
        )
        if user_exists:
            user = ECOMUser.objects.get(email=email)
            if user:
                if user.is_active:
                    if EncryptionServices().decrypt(user.password) == password:
                        token = TokenGenerator().get_tokens_for_user(user)
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
