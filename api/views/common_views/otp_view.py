import logging

from drf_spectacular.utils import extend_schema
from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyVerifiedError,
    EmailNotSentError,
)
from api.models.response_data_types.response_data import ResponseData
from api.models.user_models.user import ECOMUser
from api.services.definitions import DEFAULT_VERIFICATION_MESSAGE

from api.services.helpers import validate_email_format
from api.services.otp_services.otp_services import OTPServices


class SendOTPView(APIView):
    renderer_classes = [JSONRenderer]

    @extend_schema(
        responses={200: ResponseData},
    )
    def post(self, request: Request):
        try:
            request_data = request.data
            email = request_data.get("email")
            if email and validate_email_format(email):
                user_exists = (
                    True if ECOMUser.objects.filter(email=email).count() > 0 else False
                )

                if user_exists:
                    user = ECOMUser.objects.get(email=email)
                    if not user.is_active:
                        response = OTPServices().send_otp_to_user(email)
                        if response == "OK":
                            response_data = ResponseData(
                                successMessage=DEFAULT_VERIFICATION_MESSAGE
                            )
                            return Response(
                                data=response_data.model_dump(),
                                status=status.HTTP_200_OK,
                                content_type="application/json",
                            )
                        else:
                            raise EmailNotSentError()
                    else:
                        raise UserAlreadyVerifiedError()
                else:
                    raise UserNotFoundError()
            else:
                raise ValueError("Email address is not in correct format.")
        except EmailNotSentError as e:
            error_message = f"EmailNotSentError: {e.msg}"
            logging.warning(error_message)
            response_data = ResponseData(errorMessage=error_message)
            return Response(
                data=response_data.model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except UserAlreadyVerifiedError as e:
            error_message = f"UserAlreadyVerifiedError: {e.msg}"
            logging.warning(error_message)
            response_data = ResponseData(errorMessage=error_message)
            return Response(
                data=response_data.model_dump(),
                status=status.HTTP_401_UNAUTHORIZED,
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
        except ValueError as e:
            return Response(
                data={"successMessage": None, "errorMessage": f"ValueError: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
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
                data={
                    "successMessage": None,
                    "errorMessage": f"InternalServerError: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
