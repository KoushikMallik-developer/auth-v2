import os
from typing import Optional
from dotenv import load_dotenv
from psycopg2 import DatabaseError

from api.auth_exceptions.user_exceptions import (
    EmailNotSentError,
    UserNotFoundError,
    OTPNotVerifiedError,
    UserAlreadyVerifiedError,
)
from api.models.request_data_types.add_delivery_address import (
    AddDeliveryAddressRequestType,
)
from api.models.request_data_types.change_password import ChangePasswordRequestType
from api.models.request_data_types.create_user import CreateUserRequestType
from api.models.request_data_types.sign_in import SignInRequestType
from api.models.request_data_types.update_user_profile import (
    UpdateUserProfileRequestType,
)
from api.models.request_data_types.verify_otp import VerifyOTPRequestType
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
    validate_email_format,
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
    def create_new_user_service(request_data: CreateUserRequestType) -> dict:
        user: ECOMUser = ECOMUserSerializer().create(data=request_data.model_dump())
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
    def sign_in_user(request_data: SignInRequestType) -> dict:
        response = ECOMUser.authenticate_user(request_data=request_data)
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
    def change_password(uid: str, request_data: ChangePasswordRequestType):
        user = ECOMUser.objects.get(id=uid)
        if validate_password(
            request_data.password1, request_data.password2
        ).is_validated:
            user.password = EncryptionServices().encrypt(request_data.password1)
            user.save()
        else:
            raise ValueError("Passwords are not matching or not in correct format.")

    @staticmethod
    def update_user_profile(uid: str, request_data: UpdateUserProfileRequestType):
        user = ECOMUser.objects.get(id=uid)
        if not user.get_is_regular:
            raise UserNotFoundError()
        if (
            request_data.image
            and request_data.image != ""
            and request_data.image != user.image
        ):
            user.image = request_data.image
        if (
            request_data.fname
            and request_data.fname != ""
            and request_data.fname != user.fname
        ):
            if validate_name(request_data.fname).is_validated:
                user.fname = request_data.fname
        if (
            request_data.lname
            and request_data.lname != ""
            and request_data.lname != user.lname
        ):
            if validate_name(request_data.lname).is_validated:
                user.lname = request_data.lname
        if (
            request_data.dob
            and request_data.dob != ""
            and request_data.dob != user.fname
        ):
            dob = string_to_datetime(request_data.dob)
            if validate_dob(dob).is_validated:
                user.dob = dob
        if (
            request_data.phone
            and request_data.phone != ""
            and request_data.phone != user.phone
        ):
            if validate_phone(phone=request_data.phone).is_validated:
                user.phone = request_data.phone
        user.save()

    def update_delivery_address(
        self, uid: str, address_uid: str, request_data: AddDeliveryAddressRequestType
    ):
        if DeliveryAddress.objects.filter(id=address_uid, user__id=uid).exists():
            address: DeliveryAddress = DeliveryAddress.objects.get(
                id=address_uid, user__id=uid
            )
        else:
            raise ValueError("Address not found.")
        address_line1 = request_data.address_line1
        address_line2 = request_data.address_line2
        state = request_data.state
        city = request_data.city
        country = request_data.country
        pin = request_data.pin
        landmark = request_data.landmark
        address_type = request_data.address_type
        is_default = request_data.is_default
        delivery_to_phone = request_data.delivery_to_phone
        delivery_to_person_name = request_data.delivery_to_person_name
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
            self.handle_default_address_update()
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

    def add_delivery_address(
        self, uid: str, request_data: AddDeliveryAddressRequestType
    ):
        user = ECOMUser.objects.get(id=uid)
        if not user.get_is_regular:
            raise UserNotFoundError()
        address = DeliveryAddress()
        address.user = user
        address_line1 = request_data.address_line1
        address_line2 = request_data.address_line2
        state = request_data.state
        city = request_data.city
        country = request_data.country
        pin = request_data.pin
        landmark = request_data.landmark
        address_type = request_data.address_type
        is_default = request_data.is_default
        delivery_to_phone = request_data.delivery_to_phone
        delivery_to_person_name = request_data.delivery_to_person_name

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
            self.handle_default_address_update()
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

    @staticmethod
    def verify_user_with_otp(request_data: VerifyOTPRequestType):
        email = request_data.email
        otp = request_data.otp
        if email and validate_email_format(email) and otp and len(otp) == 6:
            user_exists = (
                True if ECOMUser.objects.filter(email=email).count() > 0 else False
            )

            if user_exists:
                user = ECOMUser.objects.get(email=email)
                user = ExportECOMUser(**user.model_to_dict())
                if not user.is_active:
                    response = OTPServices().verify_otp(user, otp)
                    if response:
                        token = TokenGenerator().get_tokens_for_user(user)
                        return token
                    else:
                        raise OTPNotVerifiedError()
                else:
                    raise UserAlreadyVerifiedError()
            else:
                raise UserNotFoundError()
        else:
            raise ValueError("Email & OTP data are invalid.")

    def handle_default_address_update(self):
        # TODO: Need to update this method to handle the default address update.
        pass
