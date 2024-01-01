from django.urls import path

from api.views.add_delivery_address import AddDeliveryAddress
from api.views.all_users import AllUsersView
from api.views.clear_server_cache import ClearServerCaches
from api.views.create_user import CreateUsersView
from api.views.otp_view import SendOTPView
from api.views.password_reset import PasswordResetView
from api.views.remove_user import RemoveUserView
from api.views.sign_in import SignInView
from api.views.update_delivery_address import UpdateDeliveryAddress
from api.views.update_password import UpdatePasswordView
from api.views.update_profile import UpdateProfileView
from api.views.user_details import UserDetailView
from api.views.validate_otp_view import ValidateOTPView

urlpatterns = [
    path("all-users", AllUsersView.as_view(), name="All-Users"),
    path("create-users", CreateUsersView.as_view(), name="Create-Users"),
    path("sign-in", SignInView.as_view(), name="sign-in"),
    path("send-otp", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp", ValidateOTPView.as_view(), name="verify-otp"),
    path(
        "reset-password",
        PasswordResetView.as_view(),
        name="send-reset-password-email",
    ),
    path("update-password", UpdatePasswordView.as_view(), name="Change-User-Password"),
    path("update-profile", UpdateProfileView.as_view(), name="Update-User-profile"),
    path("remove-user", RemoveUserView.as_view(), name="Remove-User"),
    path(
        "add-delivery-address",
        AddDeliveryAddress.as_view(),
        name="Add-Delivery-Address",
    ),
    path(
        "update-delivery-address",
        UpdateDeliveryAddress.as_view(),
        name="Add-Delivery-Address",
    ),
    path("user-details", UserDetailView.as_view(), name="user-details"),
    path("clear-caches", ClearServerCaches.as_view(), name="clear-caches"),
]
