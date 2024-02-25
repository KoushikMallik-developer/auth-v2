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
        except NotImplementedError as e:
            logging.warning(f"Internal Server Error: {e}")
            return Response(
                data=ResponseData(
                    errorMessage=f"NotImplementedError: {e}"
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )

        except AUTHBaseException as e:
            return Response(
                data=ResponseData(errorMessage=f"{e.name}: {e.msg}").model_dump(),
                status=e.status,
                content_type="application/json",
            )
