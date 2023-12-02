import pytest
from django.forms import model_to_dict

from api.models.export_models.export_user import ExportECOMUser
from api.models.user import ECOMUser
from api.services.otp_services.otp_services import OTPServices


@pytest.mark.django_db
@pytest.mark.usefixtures("create_test_user")
class TestSendOTP:
    def test_send_otp(self):
        otp_services = OTPServices()
        user = ECOMUser.objects.get(email="koushikmallik001@gmail.com")
        user = ExportECOMUser(**model_to_dict(user))
        response = otp_services.send_otp_to_user(user=user)
        assert response
        assert response == "OK"
