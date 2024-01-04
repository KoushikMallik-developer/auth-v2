from api.auth_exceptions.user_exceptions import EmailNotSentError, UserNotFoundError
from api.models.export_types.export_seller import ExportECOMSeller
from api.models.export_types.export_user import ExportECOMUser
from api.models.request_data_types.create_seller import CreateSellerRequestType
from api.models.request_data_types.sign_in import SignInRequestType
from api.models.request_data_types.update_seller_details import (
    UpdateSellerDetailsRequestType,
)
from api.models.user_models.seller_models.address import SellerAddress
from api.models.user_models.seller_models.seller_details import ECOMSellerDetails
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
    validate_pin,
)
from api.services.otp_services.otp_services import OTPServices


class SellerServices:
    @staticmethod
    def create_new_seller(request_data: CreateSellerRequestType) -> dict:
        user = ECOMUserSerializer().create(data=request_data.model_dump())
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
        response = ECOMUser.authenticate_seller(request_data=request_data)
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

    @staticmethod
    def update_seller_details(uid: str, request_data: UpdateSellerDetailsRequestType):
        user = ECOMUser.objects.get(id=uid)
        if not user.get_is_seller:
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
        if request_data.dob and request_data.dob != "" and request_data.dob != user.dob:
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

        is_seller_details_updated = False
        if ECOMSellerDetails.objects.filter(seller__id=uid).exists():
            seller_details = ECOMSellerDetails.objects.get(seller__id=uid)
        else:
            seller_details = ECOMSellerDetails()
        if (
            request_data.company_name
            and request_data.company_name != ""
            and request_data.company_name != seller_details.company_name
        ):
            seller_details.company_name = request_data.company_name
            is_seller_details_updated = True

        if (
            request_data.bio
            and request_data.bio != ""
            and request_data.bio != seller_details.bio
        ):
            seller_details.bio = request_data.bio
            is_seller_details_updated = True

        if (
            request_data.website
            and request_data.website != ""
            and request_data.website != seller_details.website
        ):
            seller_details.website = request_data.website
            is_seller_details_updated = True

        if is_seller_details_updated:
            if not hasattr(seller_details, "seller"):
                seller_details.seller = user
            seller_details.save()

        is_seller_address_updated = False
        if SellerAddress.objects.filter(seller__id=uid).exists():
            seller_address = SellerAddress.objects.get(seller__id=uid)
        else:
            seller_address = SellerAddress()

        if (
            request_data.address_line1
            and request_data.address_line1 != ""
            and request_data.address_line1 != seller_address.address_line1
        ):
            seller_address.address_line1 = request_data.address_line1
            is_seller_address_updated = True
        if (
            request_data.address_line2
            and request_data.address_line2 != ""
            and request_data.address_line2 != seller_address.address_line2
        ):
            seller_address.address_line2 = request_data.address_line2
            is_seller_address_updated = True
        if (
            request_data.state
            and request_data.state != ""
            and isinstance(request_data.state, str)
        ):
            seller_address.state = request_data.state
            is_seller_address_updated = True
        if (
            request_data.city
            and request_data.city != ""
            and isinstance(request_data.city, str)
        ):
            seller_address.city = request_data.city
            is_seller_address_updated = True
        if (
            request_data.country
            and request_data.country != ""
            and isinstance(request_data.country, str)
        ):
            seller_address.country = request_data.country
            is_seller_address_updated = True
        if (
            request_data.pin
            and request_data.pin != ""
            and isinstance(request_data.pin, str)
        ):
            pincode_validation_result = validate_pin(request_data.pin)
            if pincode_validation_result.is_validated:
                seller_address.pin = request_data.pin
                is_seller_address_updated = True
            else:
                raise ValueError(pincode_validation_result.error)
        if (
            request_data.landmark
            and request_data.landmark != ""
            and isinstance(request_data.landmark, str)
        ):
            seller_address.landmark = request_data.landmark
            is_seller_address_updated = True

        if is_seller_address_updated:
            if not hasattr(seller_address, "seller"):
                seller_address.seller = user
            seller_address.save()

    @staticmethod
    def get_seller_details(uid: str) -> ExportECOMSeller:
        seller = ECOMUser.objects.get(id=uid)
        seller_details = ExportECOMSeller(
            with_id=False, additional_details=True, **seller.model_to_dict()
        )
        return seller_details
