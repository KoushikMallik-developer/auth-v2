import logging
from typing import Optional

from rest_framework import status

from api.auth_exceptions.base_exception import AUTHBaseException


class UserNotFoundError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_401_UNAUTHORIZED
        if not name:
            self.name = "UserNotFoundError"
        if not msg:
            self.msg = "This user is not registered. Please register as new user."
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class UserAlreadyVerifiedError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_401_UNAUTHORIZED
        if not name:
            self.name = "UserAlreadyVerifiedError"
        if not msg:
            self.msg = "This user is already verified."
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class UserNotVerifiedError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_401_UNAUTHORIZED
        if not name:
            self.name = "UserNotVerifiedError"
        if not msg:
            self.msg = "This user is not verified. Please verify your email first."
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class EmailNotSentError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if not name:
            self.name = "EmailNotSentError"
        if not msg:
            self.msg = "Verification Email could not be sent."

        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class OTPNotVerifiedError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if not name:
            self.name = "OTPNotVerifiedError"
        if not msg:
            self.msg = "OTP did not match."

        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class UserAuthenticationFailedError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if not name:
            self.name = "UserAuthenticationFailedError"
        if not msg:
            self.msg = "Password is invalid."

        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)
