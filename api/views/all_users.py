import logging

from drf_spectacular.utils import extend_schema
from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.response_data_types.response_data import ResponseData
from api.models.response_data_types.all_user_response_data_type import (
    AllUsersResponseData,
)
from api.services.user_services.user_services import UserServices


class AllUsersView(APIView):
    renderer_classes = [JSONRenderer]

    @extend_schema(
        responses={200: AllUsersResponseData},
    )
    def get(self, _):
        try:
            all_user_details = UserServices.get_all_users_service()
            if all_user_details and isinstance(all_user_details, AllUsersResponseData):
                return Response(
                    data=all_user_details.model_dump(),
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise Exception()
        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occured While Fetching all users details: {e}"
            )
            response_data = ResponseData(
                errorMessage=f"DatabaseError: Error Occured While Fetching all users details: {e}"
            )
            return Response(
                data=response_data.model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ValidationError as e:
            logging.error(
                f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
            )
            response_data = ResponseData(
                errorMessage=f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
            )
            return Response(
                data=response_data.model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except NotImplementedError as e:
            logging.warning(f"NotImplementedError: {e}")
            response_data = ResponseData(errorMessage=f"NotImplementedError: {e}")
            return Response(
                data=response_data.model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except Exception as e:
            logging.error(f"InternalServerError: {e}")
            response_data = ResponseData(errorMessage=f"InternalServerError: {e}")
            return Response(
                data=response_data.model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
