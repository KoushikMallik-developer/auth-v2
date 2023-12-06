import logging

from djongo.database import DatabaseError
from pydantic import ValidationError
from rest_framework import status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth_exceptions.user_exceptions import EmailNotSentError
from api.services.user_services import UserServices


class CreateUsersView(APIView):
    def post(self, request: Request):
        try:
            request_data = request.data
            username = request_data.get("username")
            email = request_data.get("email")
            fname = request_data.get("fname")
            lname = request_data.get("lname")
            password1 = request_data.get("password1")
            password2 = request_data.get("password2")
            if username and email and fname and lname and password1 and password2:
                result = UserServices.create_new_user_service(
                    data={
                        "username": username,
                        "email": email,
                        "fname": fname,
                        "lname": lname,
                        "password1": password1,
                        "password2": password2,
                    }
                )
                if result.get("successMessage"):
                    return Response(
                        data={
                            "successMessage": result.get("successMessage"),
                            "errorMessage": None,
                        },
                        status=status.HTTP_201_CREATED,
                        content_type="application/json",
                    )
            else:
                raise ValueError("Input data are not in correct format.")

        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occured While saving users details: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"DatabaseError: Error Occured While saving users details: {e}",
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
        except EmailNotSentError as e:
            return Response(
                data={"data": None, "errorMessage": f"EmailNotSentError: {e.msg}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ValueError as e:
            logging.warning(f"Internal Server Error: {e}")
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
