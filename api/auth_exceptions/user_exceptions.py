class UserNotFoundError(BaseException):
    def get_default_msg(self):
        return "Please register your account first to verify."


class UserAlreadyVerifiedError(BaseException):
    def get_default_msg(self):
        return "This user is already verified."


class EmailNotSentError(BaseException):
    def get_default_msg(self):
        return "Verification Email could not be sent."


class OTPNotVerifiedError(BaseException):
    def get_default_msg(self):
        return "OTP did not match."
