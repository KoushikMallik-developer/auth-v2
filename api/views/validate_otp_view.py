from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from api.models.user import ECOMUser
from api.services.otp_services.otp_services import OTPServices
from api.services.token_generator import TokenGenerator


class ValidateOTPView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        request_data = request.data
        email = request_data.get("email")
        otp = request_data.get("otp")

        user_exists = (
            True if ECOMUser.objects.filter(email=email).count() > 0 else False
        )

        if user_exists:
            user = ECOMUser.objects.get(email=email)
            if not user.is_active:
                response = OTPServices().verify_otp(user, otp)
                token = TokenGenerator().get_tokens_for_user(user)
                if response:
                    return Response(
                        data={
                            "message": response,
                            "token": token,
                            "errorMessage": None,
                        },
                        status=status.HTTP_200_OK,
                        content_type="application/json",
                    )
            else:
                return Response(
                    data={
                        "message": None,
                        "errorMessage": "This user is already verified.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                    content_type="application/json",
                )
        else:
            return Response(
                data={
                    "message": None,
                    "errorMessage": "Please register your account first to verify.",
                },
                status=status.HTTP_403_FORBIDDEN,
                content_type="application/json",
            )
