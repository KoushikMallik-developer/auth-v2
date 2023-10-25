from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.user_services import UserServices


class CreateUsersView(APIView):
    def post(self, request: Request):
        request_data = request.data
        username = request_data.get("username")
        email = request_data.get("email")
        fname = request_data.get("fname")
        lname = request_data.get("lname")
        password1 = request_data.get("password1")
        password2 = request_data.get("password2")
        if username and email and fname and lname and password1 and password2:
            result = UserServices.create_new_user_service(
                data={
                    "username": username,
                    "email": email,
                    "fname": fname,
                    "lname": lname,
                    "password1": password1,
                    "password2": password2,
                }
            )
            if result.get("error"):
                return Response(
                    data={"token": None, "errorMessage": result.get("error")},
                    status=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json",
                )
            if result.get("token"):
                return Response(
                    data={"token": result.get("token"), "errorMessage": None},
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
