from api.auth_exceptions.user_exceptions import EmailNotSentError
from api.models.export_types.export_user import ExportECOMUser
from api.models.user_models.user import ECOMUser
from api.serializers.ecom_user_serializer import ECOMUserSerializer
from api.services.definitions import (
    DEFAULT_VERIFICATION_MESSAGE,
)
from api.services.helpers import (
    validate_name,
    validate_dob,
    string_to_datetime,
    validate_phone,
)
from api.services.otp_services.otp_services import OTPServices


class SellerServices:
    @staticmethod
    def create_new_user_service(data: dict) -> dict:
        user: ExportECOMUser = ECOMUserSerializer().create(data=data)
        if user:
            response = OTPServices().send_otp_to_user(user.email)
            if response == "OK":
                return {
                    "successMessage": DEFAULT_VERIFICATION_MESSAGE,
                    "errorMessage": None,
                }
            else:
                raise EmailNotSentError()

    @staticmethod
    def sign_in_user(data: dict) -> dict:
        email = data.get("email")
        password = data.get("password")
        if email and password:
            response = ECOMUser.authenticate_seller(email=email, password=password)
            return response

    @staticmethod
    def update_user_profile(
        uid: str, fname: str, lname: str, dob: str, phone: str, image: str
    ):
        user = ECOMUser.objects.get(id=uid)
        if image and image != "" and image != user.image:
            user.image = image
        if fname and fname != "" and fname != user.fname:
            if validate_name(fname).is_validated:
                user.fname = fname
        if lname and lname != "" and lname != user.lname:
            if validate_name(lname).is_validated:
                user.lname = lname
        if dob and dob != "" and dob != user.fname:
            dob = string_to_datetime(dob)
            if validate_dob(dob).is_validated:
                user.dob = dob
        if phone and phone != "" and phone != user.phone:
            if validate_phone(phone=phone).is_validated:
                user.phone = phone
        user.save()

    @staticmethod
    def get_user_details(uid: str) -> ExportECOMUser:
        user = ECOMUser.objects.get(id=uid)
        user_details = ExportECOMUser(
            with_id=False, with_address=True, **user.model_to_dict()
        )
        return user_details
