from django.core.mail import EmailMessage

from api.models.email_types.ecom_email import ECOMEmailMessage
from api.models.export_models.export_user import ExportECOMUser


class EmailServices:
    @staticmethod
    def send_otp_email_by_user(user: ExportECOMUser, otp: str) -> str:
        email: ECOMEmailMessage = ECOMEmailMessage.create_email_by_user(
            user=user, otp=otp
        )
        email_message: EmailMessage = EmailMessage(**email.model_dump())
        email_message.send()
        return "OK"

    @staticmethod
    def send_otp_email_by_user_email(user_email: str, otp: str) -> str:
        email: ECOMEmailMessage = ECOMEmailMessage.create_email_by_user_email(
            user_email=user_email, otp=otp
        )
        email_message: EmailMessage = EmailMessage(**email.model_dump())
        email_message.send()
        return "OK"
