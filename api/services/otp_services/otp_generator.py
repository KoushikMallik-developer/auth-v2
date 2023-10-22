import random
import string


class OTPGenerator:
    def __init__(self):
        self.length: int = 6  # specified length

    def generate_otp(self) -> str:
        # Generate a random OTP with the specified length
        digits = string.digits
        otp = "".join(random.choice(digits) for _ in range(self.length))
        return otp
