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
        try:
            user = ECOMUser.objects.get(email=email)
            if user.is_active:
                if EncryptionServices().decrypt(user.password) == password:
                    token = TokenGenerator().get_tokens_for_user(user)
                    return {
                        "token": token,
                        "errorMessage": None,
                    }
                else:
                    return {
                        "token": None,
                        "errorMessage": "Invalid Password.",
                    }
            else:
                return {
                    "token": None,
                    "errorMessage": "Please verify your email first.",
                }
        except Exception:
            return {
                "token": None,
                "errorMessage": "User doesn't exist. Please sign up your account.",
            }
