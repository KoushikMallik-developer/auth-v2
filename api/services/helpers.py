import re

from api.models.user import ECOMUser
from api.models.validation_result import ValidationResult


def validate_email(email: str) -> ValidationResult:
    if validate_email_format(email):
        existing_account = ECOMUser.objects.filter(email=email).exists()
        if existing_account:
            return ValidationResult(
                is_validated=False,
                error="An account with this email id is already existed.",
            )
        return ValidationResult(is_validated=True, error=None)
    else:
        return ValidationResult(is_validated=False, error="Email format is not correct")


def validate_email_format(email: str) -> bool:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def validate_name(name: str) -> ValidationResult:
    if name.lower().isalpha():
        return ValidationResult(is_validated=True, error=None)
    else:
        return ValidationResult(
            is_validated=False, error="First name or Last name can only have alphabets"
        )


def validate_username(username: str) -> ValidationResult:
    """Checks if the received username matches the required conditions."""
    # Usernames can't be shorter than minlen
    if len(username) < 6:
        return ValidationResult(
            is_validated=False, error="Usernames can't be shorter than 6 characters"
        )
    # Usernames can only use letters, numbers, dots and underscores
    if not re.match("^[a-z0-9._]*$", username):
        return ValidationResult(
            is_validated=False,
            error="Usernames can only use letters, numbers, dots and underscores",
        )
    # Usernames can't begin with a number
    if username[0].isnumeric():
        return ValidationResult(
            is_validated=False, error="Usernames can't begin with a number"
        )
    return ValidationResult(is_validated=True, error=None)


def validate_password(password1: str, password2: str) -> ValidationResult:
    if password1 == password2:
        if len(password1) > 6:
            return ValidationResult(is_validated=True, error=None)
        return ValidationResult(
            is_validated=False, error="Password must be minimum of 6 characters"
        )
    else:
        return ValidationResult(is_validated=False, error="Passwords did not match")
