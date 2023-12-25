from enum import Enum

default_email = "shoopixa.server@gmail.com"
DEFAULT_VERIFICATION_MESSAGE = (
    "Verification Email has been sent successfully to the user. Please verify your email to"
    " access the account."
)


class EnvironmentSettings(Enum):
    dev = "DEV"
    stg = "STAGING"
    prod = "PRODUCTION"
    qa = "QA"
