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
        except UserAlreadyVerifiedError as e:
            return Response(
                data={"data": None, "errorMessage": f"Internal Server Error: {e.msg}"},
                status=status.HTTP_403_FORBIDDEN,
                content_type="application/json",
            )
        except UserNotFoundError as e:
            return Response(
                data={"data": None, "errorMessage": f"Internal Server Error: {e.msg}"},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        except ValueError as e:
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
                data={"data": None, "errorMessage": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except Exception as e:
            return Response(
                data={"data": None, "errorMessage": f"ValueError: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
