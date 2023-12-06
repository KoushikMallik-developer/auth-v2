import logging

from djongo.database import DatabaseError
from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.export_models.export_user import ExportECOMUserList
from api.services.user_services import UserServices


class AllUsersView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request: Request):
        try:
            all_user_details = UserServices.get_all_users_service()
            if all_user_details and isinstance(all_user_details, ExportECOMUserList):
                return Response(
                    data={"data": all_user_details.model_dump(), "errorMessage": None},
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise Exception()
        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occured While Fetching all users details: {e}"
            )
            return Response(
                data={
                    "data": None,
                    "errorMessage": f"DatabaseError: Error Occured While Fetching all users details: {e}",
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
                    "data": None,
                    "errorMessage": f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            logging.error(f"InternalServerError: {e}")
            return Response(
                data={"data": None, "errorMessage": f"InternalServerError {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
