from rest_framework_simplejwt.tokens import RefreshToken

from api.models.export_models.export_user import ExportECOMUser


class TokenGenerator:
    def get_tokens_for_user(self, user: ExportECOMUser) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
