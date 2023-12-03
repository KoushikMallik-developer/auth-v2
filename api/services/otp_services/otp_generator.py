import random
import string
from typing import Optional


class OTPGenerator:
    def __init__(self):
        self.length: int = 6  # specified length

    def generate_otp(self, length: Optional[int] = None) -> str:
        # Generate a random OTP with the specified length
        if length:
            self.length = length
        digits = string.digits
        otp = "".join(random.choice(digits) for _ in range(self.length))
        return otp
