import logging
from drf_spectacular.utils import extend_schema
from psycopg2 import DatabaseError
from dns.resolver import NXDOMAIN, LifetimeTimeout, YXDOMAIN, NoAnswer, NoNameservers
from pydantic import ValidationError
from rest_framework import status, serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth_exceptions.user_exceptions import EmailNotSentError
from api.models.request_data_types.create_user import CreateUserRequestType
from api.models.response_data_types.response_data import ResponseData
from api.services.user_services.user_services import UserServices


class CreateUsersView(APIView):
    renderer_classes = [JSONRenderer]

    @extend_schema(
        request=CreateUserRequestType,
        responses={200: ResponseData},
    )
    def post(self, request: Request):
        try:
            result: ResponseData = UserServices.create_new_user_service(
                request_data=CreateUserRequestType(**request.data)
            )
            return Response(
                data=result.model_dump(),
                status=status.HTTP_201_CREATED,
                content_type="application/json",
            )
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
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailNotSentError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except NXDOMAIN as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailDoesNotExistsError: {e.msg}",
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except NoNameservers as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailDoesNotExistsError: {e.msg}",
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except NoAnswer as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailDoesNotExistsError: {e.msg}",
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except YXDOMAIN as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailDoesNotExistsError: {e.msg}",
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )
        except LifetimeTimeout as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailDoesNotExistsError: {e.msg}",
                },
                status=status.HTTP_400_BAD_REQUEST,
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
