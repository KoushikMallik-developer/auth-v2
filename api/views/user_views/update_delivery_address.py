import logging

from psycopg2 import DatabaseError
from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
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
from api.services.helpers import decode_jwt_token, validate_user_uid
from api.services.user_services.user_services import UserServices


class UpdateDeliveryAddress(APIView):
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(
        operation_summary="Update-Delivery-Address",
        operation_description="Update-Delivery-Address",
        request_body=Schema(
            title="Update-Delivery-Address Request",
            type=openapi.TYPE_OBJECT,
            properties={
                "address_uid": Schema(
                    name="address_uid",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "address_line1": Schema(
                    name="address_line1",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "address_line2": Schema(
                    name="address_line2",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "city": Schema(
                    name="city",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "state": Schema(
                    name="state",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "country": Schema(
                    name="country",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "pin": Schema(
                    name="pin",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "landmark": Schema(
                    name="landmark",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "address_type": Schema(
                    name="address_type",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "is_default": Schema(
                    name="is_default",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "delivery_to_phone": Schema(
                    name="delivery_to_phone",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
                "delivery_to_person_name": Schema(
                    name="delivery_to_person_name",
                    in_=openapi.IN_BODY,
                    type=openapi.TYPE_STRING,
                ),
            },
        ),
        responses={
            201: Schema(
                title="Add-Delivery-Address Response",
                type=openapi.TYPE_OBJECT,
                properties={
                    "successMessage": Schema(
                        name="successMessage",
                        in_=openapi.IN_BODY,
                        type=openapi.TYPE_STRING,
                    ),
                    "errorMessage": Schema(
                        name="errorMessage",
                        in_=openapi.IN_BODY,
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
            "default": Schema(
                title="Add-Delivery-Address Response",
                type=openapi.TYPE_OBJECT,
                properties={
                    "successMessage": Schema(
                        name="successMessage",
                        in_=openapi.IN_BODY,
                        type=openapi.TYPE_STRING,
                    ),
                    "errorMessage": Schema(
                        name="errorMessage",
                        in_=openapi.IN_BODY,
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
        },
    )
    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                UserServices().update_delivery_address(
                    uid=user_id,
                    address_uid=request.data.get("address_uid"),
                    request_data=AddDeliveryAddressRequestType(**request.data),
                )
                return Response(
                    data={
                        "successMessage": "Delivery Address details updated successfully.",
                        "errorMessage": None,
                    },
                    status=status.HTTP_200_OK,
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
