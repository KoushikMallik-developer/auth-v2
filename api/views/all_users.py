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
        all_user_details = UserServices().get_all_users_service()
        if all_user_details and isinstance(all_user_details, ExportECOMUserList):
            return Response(
                data={"data": all_user_details.dict(), "errorMessage": None},
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        else:
            return Response(
                data={"data": None, "errorMessage": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
