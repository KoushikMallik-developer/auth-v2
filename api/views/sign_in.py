from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.user_services import UserServices


class SignInView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        request_data = request.data
        email = request_data.get("email")
        password = request_data.get("password")

        if email and password:
            result = UserServices.sign_in_user(
                data={
                    "email": email,
                    "password": password,
                }
            )
            if result.get("errorMessage"):
                return Response(
                    data={"token": None, "errorMessage": result.get("errorMessage")},
                    status=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json",
                )
            if result.get("token"):
                return Response(
                    data={"token": result.get("token"), "errorMessage": None},
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
