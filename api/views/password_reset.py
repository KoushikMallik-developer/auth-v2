import logging

from djongo.database import DatabaseError
from pydantic import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers


from api.auth_exceptions.user_exceptions import (
    EmailNotSentError,
    UserNotFoundError,
    UserAuthenticationFailedError,
    UserNotVerifiedError,
)
from api.services.user_services import UserServices


class PasswordResetView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            email = request.data["email"]
            if email:
                result = UserServices().reset_password(email=email)
                return Response(
                    data={
                        "successMessage": result.get("successMessage"),
                        "errorMessage": None,
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise ValueError("Email format is not correct.")
        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occured While fetching user details: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"DatabaseError: Error Occured While fetching user details: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ValidationError as e:
            logging.error(
                f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except EmailNotSentError as e:
            return Response(
                data={"data": None, "errorMessage": f"EmailNotSentError: {e.msg}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except UserAuthenticationFailedError as e:
            return Response(
                data={
                    "data": None,
                    "errorMessage": f"UserAuthenticationFailedError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except UserNotFoundError as e:
            return Response(
                data={"data": None, "errorMessage": f"UserNotFoundError: {e.msg}"},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        except UserNotVerifiedError as e:
            return Response(
                data={"data": None, "errorMessage": f"UserNotVerifiedError: {e.msg}"},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        except serializers.ValidationError as e:
            logging.warning(f"SerializerValidationError: {e.detail}")
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"SerializerValidationError: {'; '.join([error for error in e.detail])}",
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except ValueError as e:
            logging.warning(f"ValueError: {e}")
            return Response(
                data={"successMessage": None, "errorMessage": f"ValueError: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except NotImplementedError as e:
            logging.warning(f"Internal Server Error: {e}")
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
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
