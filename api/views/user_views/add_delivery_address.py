import logging

from drf_spectacular.utils import extend_schema
from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from api.auth_exceptions.user_exceptions import (
    EmailNotSentError,
    UserAuthenticationFailedError,
    UserNotFoundError,
    UserNotVerifiedError,
)
from api.models.request_data_types.add_delivery_address import (
    AddDeliveryAddressRequestType,
)
from api.models.response_data_types.response_data import ResponseData
from api.services.helpers import decode_jwt_token, validate_user_uid
from api.services.user_services.user_services import UserServices


class AddDeliveryAddress(APIView):
    renderer_classes = [JSONRenderer]

    @extend_schema(request=AddDeliveryAddressRequestType, responses={200: ResponseData})
    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                UserServices().add_delivery_address(
                    uid=user_id,
                    request_data=AddDeliveryAddressRequestType(**request.data),
                )
                data = ResponseData(successMessage="Address added successfully.")
                return Response(
                    data=data.model_dump(),
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except TokenError as e:
            logging.error(f"TokenError: {str(e)}")
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"TokenError: {str(e)}",
                },
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        except DatabaseError as e:
            logging.error(f"DatabaseError: Error Occured While fetching details: {e}")
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"DatabaseError: Error Occured While fetching details: {e}",
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
                data={
                    "successMessage": None,
                    "errorMessage": f"EmailNotSentError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except UserAuthenticationFailedError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"UserAuthenticationFailedError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except UserNotFoundError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"UserNotFoundError: {e.msg}",
                },
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        except UserNotVerifiedError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"UserNotVerifiedError: {e.msg}",
                },
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
