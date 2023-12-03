import base64
from typing import Optional

from django.core.cache import cache
from django.utils import timezone

from api.models.email_verification import ECOMEmailVerification
from api.models.export_models.export_user import ExportECOMUser
from api.models.user import ECOMUser
from api.services.email_services import EmailServices
from api.services.otp_services.otp_generator import OTPGenerator


class OTPServices:
    def __init__(self):
        self.KEYWORD_PREFIX = "_VERIFICATION_OTP"
        self.expiration_time = 900

    def send_otp_to_user(self, user: ExportECOMUser) -> Optional[str]:
        email_services = EmailServices()
        cache_keyword = f"{user.email.upper()}{self.KEYWORD_PREFIX}"
        cached_data = cache.get(cache_keyword)
        db_user = ECOMUser.objects.get(email=user.email)
        if cached_data:
            response = email_services.send_otp_email_by_user(
                user=user, otp=base64.b64decode(cached_data).decode("utf-8")
            )
        elif (
            ECOMEmailVerification.objects.filter(
                user=db_user, expiration_time__gte=timezone.now()
            ).count()
            > 0
        ):
            verification_data: ECOMEmailVerification = (
                ECOMEmailVerification.objects.get(
                    user=db_user, expiration_time__gte=timezone.now()
                )
            )
            cache.set(
                cache_keyword,
                base64.b64encode(verification_data.code.encode("utf-8")),
                self.expiration_time,
            )
            response = email_services.send_otp_email_by_user(
                user=user, otp=verification_data.code
            )
        else:
            verification_data: ECOMEmailVerification = self.__create_otp(user=db_user)
            cache.set(
                cache_keyword,
                base64.b64encode(verification_data.code.encode("utf-8")),
                self.expiration_time,
            )
            response = email_services.send_otp_email_by_user(
                user=user, otp=verification_data.code
            )

        if response == "OK":
            return response

    def __create_otp(self, user: ECOMUser) -> ECOMEmailVerification:
        generator = OTPGenerator()
        code = generator.generate_otp()
        ecom_verification_obj = ECOMEmailVerification(user=user, code=code)
        ecom_verification_obj.save()
        return ecom_verification_obj

    def __validate_otp(self, user: ECOMUser, otp) -> bool:
        try:
            ecom_verification_obj = ECOMEmailVerification.objects.get(
                user=user, code=otp, is_used=False, expiration_time__gte=timezone.now()
            )
            ecom_verification_obj.is_used = True
            ecom_verification_obj.save()
            return True
        except ECOMEmailVerification.DoesNotExist:
            return False

    def verify_otp(self, user: ExportECOMUser, otp) -> str:
        user = ECOMUser.objects.get(email=user.email)
        if self.__validate_otp(user=user, otp=otp):
            user.is_verified = True
            user.save()
            return "Account Verification completed Successfully"
        else:
            return "Account Verification Failed, Please try again."
