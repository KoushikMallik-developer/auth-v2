import logging

from drf_spectacular.utils import extend_schema
from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth_exceptions.base_exception import AUTHBaseException
from api.auth_exceptions.ecom_exception import EcomValueError
from api.models.request_data_types.sign_in import SignInRequestType
from api.models.response_data_types.response_data import ResponseData
from api.models.response_data_types.sign_in import SignInResponseData, VerificationToken
from api.services.user_services.user_services import UserServices


class SignInView(APIView):
    renderer_classes = [JSONRenderer]

    @extend_schema(request=SignInRequestType, responses={200: SignInResponseData})
    def post(self, request: Request):
        try:
            request_data = request.data
            email = request_data.get("email")
            password = request_data.get("password")

            if email and password:
                result = UserServices.sign_in_user(
                    request_data=SignInRequestType(**request_data)
                )
                if result.get("token"):
                    data = SignInResponseData(
                        token=VerificationToken(**result.get("token"))
                    )

                    return Response(
                        data=data.model_dump(),
                        status=status.HTTP_200_OK,
                        content_type="application/json",
                    )
            else:
                raise EcomValueError(msg="Email or Password is not in correct format")
        except AUTHBaseException as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"{e.name}: {e.msg}",
                },
                status=e.status,
                content_type="application/json",
            )
        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occured While saving users details: {e}"
            )
            return Response(
                data=ResponseData(
                    errorMessagee=f"DatabaseError: Error Occured While saving users details: {e}",
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ValidationError as e:
            logging.error(
                f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
            )
            return Response(
                data=ResponseData(
                    errorMessage=f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
