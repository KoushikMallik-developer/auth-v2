import logging

from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyVerifiedError,
    OTPNotVerifiedError,
    EmailNotSentError,
)
from api.models.user import ECOMUser
from api.services.helpers import validate_email_format
from api.services.otp_services.otp_services import OTPServices
from api.services.token_generator import TokenGenerator


class ValidateOTPView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            request_data = request.data
            email = request_data.get("email")
            otp = request_data.get("otp")
            if email and validate_email_format(email) and len(otp) == 6:
                user_exists = (
                    True if ECOMUser.objects.filter(email=email).count() > 0 else False
                )

                if user_exists:
                    user = ECOMUser.objects.get(email=email)
                    if not user.is_active:
                        response = OTPServices().verify_otp(user, otp)
                        if response:
                            token = TokenGenerator().get_tokens_for_user(user)
                            return Response(
                                data={
                                    "token": token,
                                    "errorMessage": None,
                                },
                                status=status.HTTP_200_OK,
                                content_type="application/json",
                            )
                        else:
                            raise OTPNotVerifiedError()
                    else:
                        raise UserAlreadyVerifiedError()
                else:
                    raise UserNotFoundError()
            else:
                raise ValueError("Email & OTP data are invalid.")
        except EmailNotSentError as e:
            return Response(
                data={"data": None, "errorMessage": f"EmailNotSentError: {e.msg}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except UserAlreadyVerifiedError as e:
            return Response(
                data={
                    "data": None,
                    "errorMessage": f"UserAlreadyVerifiedError: {e.msg}",
                },
                status=status.HTTP_403_FORBIDDEN,
                content_type="application/json",
            )
        except UserNotFoundError as e:
            return Response(
                data={"data": None, "errorMessage": f"UserNotFoundError: {e.msg}"},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        except ValueError as e:
            logging.error(f"ValueError: {e}")
            return Response(
                data={"data": None, "errorMessage": f"ValueError: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except ValidationError as e:
            logging.error(
                f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
            )
            return Response(
                data={
                    "data": None,
                    "errorMessage": f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except NotImplementedError as e:
            logging.warning(f"NotImplementedError: {e}")
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"NotImplementedError: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except Exception as e:
            logging.warning(f"InternalServerError: {e}")
            return Response(
                data={"data": None, "errorMessage": f"InternalServerError: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
