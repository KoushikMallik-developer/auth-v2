import os
from typing import Optional
from dotenv import load_dotenv
from psycopg2 import DatabaseError

from api.auth_exceptions.user_exceptions import EmailNotSentError, UserNotFoundError
from api.models.user_models.delivery_address import DeliveryAddress
from api.models.export_types.export_user import ExportECOMUser, ExportECOMUserList
from api.models.user_models.user import ECOMUser
from api.serializers.ecom_user_serializer import ECOMUserSerializer
from api.services.definitions import (
    DEFAULT_VERIFICATION_MESSAGE,
    TRUTH_LIST,
)
from api.services.email_services.email_services import EmailServices
from api.services.encryption_services.encryption_service import EncryptionServices
from api.services.helpers import (
    validate_user_email,
    validate_password,
    validate_name,
    validate_dob,
    string_to_datetime,
    validate_phone,
    validate_pin,
)
from api.services.otp_services.otp_services import OTPServices
from api.services.token_services.token_generator import TokenGenerator


class UserServices:
    @staticmethod
    def get_all_users_service() -> Optional[ExportECOMUserList]:
        try:
            users = ECOMUser.objects.all()
        except Exception:
            raise DatabaseError()
        if users:
            all_user_details = []
            for user in users:
                user_export_details = ExportECOMUser(
                    with_id=False, **user.model_to_dict()
                )
                all_user_details.append(user_export_details)
            all_user_details = ExportECOMUserList(user_list=all_user_details)
            return all_user_details
        else:
            return None

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
            response = ECOMUser.authenticate(email=email, password=password)
            return response

    def reset_password(self, email: str) -> dict:
        if validate_user_email(email=email).is_validated:
            reset_url = self.generate_reset_password_url(email=email)
            if (
                EmailServices.send_password_reset_email_by_user_email(
                    user_email=email, reset_url=reset_url
                )
                == "OK"
            ):
                return {
                    "successMessage": "Password reset link sent successfully.",
                    "errorMessage": None,
                }
            else:
                raise EmailNotSentError()
        else:
            raise UserNotFoundError()

    @staticmethod
    def generate_reset_password_url(email: str) -> str:
        user = ECOMUser.objects.get(email=email)
        token = (
            TokenGenerator()
            .get_tokens_for_user(ExportECOMUser(**user.model_to_dict()))
            .get("access")
        )
        load_dotenv()
        FRONTEND_BASE_URL = os.environ.get("FRONTEND_BASE_URL")
        reset_url = f"{FRONTEND_BASE_URL}/password-reset/{token}/"
        return reset_url

    @staticmethod
    def change_password(uid: str, password1: str, password2: str):
        user = ECOMUser.objects.get(id=uid)
        if validate_password(password1, password2).is_validated:
            user.password = EncryptionServices().encrypt(password1)
            user.save()
        else:
            raise ValueError("Passwords are not matching or not in correct format.")

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
    def update_delivery_address(
        uid: str,
        address_uid: str,
        address_line1: str,
        address_line2: str,
        state: str,
        city: str,
        country: str,
        pin: str,
        landmark: str,
        address_type: str,
        is_default: str,
        delivery_to_phone: str,
        delivery_to_person_name: str,
    ):
        if DeliveryAddress.objects.filter(id=address_uid, user__id=uid).exists():
            address: DeliveryAddress = DeliveryAddress.objects.get(
                id=address_uid, user__id=uid
            )
        else:
            raise ValueError("Address not found.")
        if (
            address_line1
            and address_line1 != ""
            and address_line1 != address.address_line1
        ):
            address.address_line1 = address_line1
        if (
            address_line2
            and address_line2 != ""
            and address_line2 != address.address_line2
        ):
            address.address_line2 = address_line2
        if state and state != "" and isinstance(state, str):
            address.state = state
        if city and city != "" and isinstance(city, str):
            address.city = city
        if country and country != "" and isinstance(country, str):
            address.country = country
        if pin and pin != "" and isinstance(pin, str):
            pincode_validation_result = validate_pin(pin)
            if pincode_validation_result.is_validated:
                address.pin = pin
            else:
                raise ValueError(pincode_validation_result.error)
        if landmark and landmark != "" and isinstance(landmark, str):
            address.landmark = landmark
        if address_type and address_type != "" and isinstance(address_type, str):
            address.address_type = address_type
        if is_default in TRUTH_LIST:
            address.is_default = is_default
        if (
            delivery_to_phone
            and delivery_to_phone != ""
            and isinstance(delivery_to_phone, str)
        ):
            if validate_phone(phone=delivery_to_phone).is_validated:
                address.delivery_to_phone = delivery_to_phone
            else:
                raise ValueError("Phone Number is not valid.")
        if (
            delivery_to_person_name
            and delivery_to_person_name != ""
            and isinstance(delivery_to_person_name, str)
        ):
            address.delivery_to_person_name = delivery_to_person_name
        address.save()

    @staticmethod
    def add_delivery_address(
        uid: str,
        address_line1: str,
        address_line2: str,
        state: str,
        city: str,
        country: str,
        pin: str,
        landmark: str,
        address_type: str,
        is_default: str,
        delivery_to_phone: str,
        delivery_to_person_name: str,
    ):
        user = ECOMUser.objects.get(id=uid)
        address = DeliveryAddress()
        address.user = user
        if address_line1 and address_line1 != "" and isinstance(address_line1, str):
            address.address_line1 = address_line1
        if address_line2 and address_line2 != "" and isinstance(address_line2, str):
            address.address_line2 = address_line2
        if state and state != "" and isinstance(state, str):
            address.state = state
        if city and city != "" and isinstance(city, str):
            address.city = city
        if country and country != "" and isinstance(country, str):
            address.country = country
        if pin and pin != "" and isinstance(pin, str):
            pincode_validation_result = validate_pin(pin)
            if pincode_validation_result.is_validated:
                address.pin = pin
            else:
                raise ValueError(pincode_validation_result.error)
        if landmark and landmark != "" and isinstance(landmark, str):
            address.landmark = landmark
        if address_type and address_type != "" and isinstance(address_type, str):
            address.address_type = address_type
        if is_default in TRUTH_LIST:
            address.is_default = is_default
        if (
            delivery_to_phone
            and delivery_to_phone != ""
            and isinstance(delivery_to_phone, str)
        ):
            if validate_phone(phone=delivery_to_phone).is_validated:
                address.delivery_to_phone = delivery_to_phone
            else:
                raise ValueError("Phone Number is not valid.")
        if (
            delivery_to_person_name
            and delivery_to_person_name != ""
            and isinstance(delivery_to_person_name, str)
        ):
            address.delivery_to_person_name = delivery_to_person_name
        if (
            address.address_line1
            and address.city
            and address.state
            and address.country
            and address.pin
            and address.delivery_to_phone
            and address.delivery_to_person_name
        ):
            address.save()
        else:
            raise ValueError("Address details are not valid.")

    @staticmethod
    def get_user_details(uid: str) -> ExportECOMUser:
        user = ECOMUser.objects.get(id=uid)
        user_details = ExportECOMUser(
            with_id=False, with_address=True, **user.model_to_dict()
        )
        return user_details
