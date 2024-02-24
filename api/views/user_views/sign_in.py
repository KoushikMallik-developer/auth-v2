import logging

from drf_spectacular.utils import extend_schema
from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import status, serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth_exceptions.base_exception import AUTHBaseException
from api.models.request_data_types.sign_in import SignInRequestType
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
                raise ValueError("Email or Password is not in correct format")

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
        except AUTHBaseException as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"{e.name}: {e.msg}",
                },
                status=e.status,
                content_type="application/json",
            )
        # except EmailNotSentError as e:
        #     return Response(
        #         data={
        #             "successMessage": None,
        #             "errorMessage": f"EmailNotSentError: {e.msg}",
        #         },
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         content_type="application/json",
        #     )
        # except UserAuthenticationFailedError as e:
        #     return Response(
        #         data={
        #             "successMessage": None,
        #             "errorMessage": f"UserAuthenticationFailedError: {e.msg}",
        #         },
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         content_type="application/json",
        #     )
        # except UserNotFoundError as e:
        #     return Response(
        #         data={
        #             "successMessage": None,
        #             "errorMessage": f"UserNotFoundError: {e.msg}",
        #         },
        #         status=status.HTTP_401_UNAUTHORIZED,
        #         content_type="application/json",
        #     )
        # except UserNotVerifiedError as e:
        #     return Response(
        #         data={
        #             "successMessage": None,
        #             "errorMessage": f"UserNotVerifiedError: {e.msg}",
        #         },
        #         status=status.HTTP_401_UNAUTHORIZED,
        #         content_type="application/json",
        #     )
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
