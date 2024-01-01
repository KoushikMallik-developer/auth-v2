from __future__ import annotations
from typing import Optional, List

from pydantic import BaseModel

from api.models.export_types.export_user import ExportECOMUser
from api.models.user_models.user import ECOMUser
from api.services.definitions import default_email
from api.services.helpers import validate_user_email


class ECOMEmailMessage(BaseModel):
    subject: str
    body: str
    from_email: Optional[str]
    to: List[str]
    bcc: Optional[str] = None
    attachments: Optional[str] = None
    headers: Optional[str] = None
    cc: Optional[str] = None
    reply_to: Optional[str] = None

    @classmethod
    def create_otp_email_by_user(
        cls, user: ExportECOMUser, otp: str
    ) -> ECOMEmailMessage:
        return cls(
            subject="Shoopixa User Verification",
            body=f"Your OTP is: {otp}",
            from_email=default_email,
            to=[user.email],
        )

    @classmethod
    def create_otp_email_by_user_email(
        cls, user_email: str, otp: str
    ) -> ECOMEmailMessage:
        if user_email:
            if ECOMUser.objects.filter(email=user_email).count() > 0:
                return cls(
                    subject="Shoopixa User Verification",
                    body=f"Your OTP is: {otp}",
                    from_email=default_email,
                    to=[user_email],
                )
            else:
                raise ValueError
        else:
            raise ValueError

    @classmethod
    def create_password_reset_email_by_user_email(
        cls, user_email: str, reset_url: str
    ) -> ECOMEmailMessage:
        if user_email:
            if validate_user_email(user_email).is_validated:
                return cls(
                    subject="Shoopixa User Password Reset",
                    body=f"Click the following link to reset your password: {reset_url}",
                    from_email=default_email,
                    to=[user_email],
                )
            else:
                raise ValueError
        else:
            raise ValueError
