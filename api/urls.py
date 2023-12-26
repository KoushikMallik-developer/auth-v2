from django.urls import path

from api.views.add_delivery_address import AddDeliveryAddress
from api.views.all_users import AllUsersView
from api.views.create_user import CreateUsersView
from api.views.otp_view import SendOTPView
from api.views.password_reset import PasswordResetView
from api.views.remove_user import RemoveUserView
from api.views.sign_in import SignInView
from api.views.update_password import UpdatePasswordView
from api.views.update_profile import UpdateProfileView
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
]
# path('login', UserLoginView.as_view(), name="User Login"),
# path('profile', UserProfileView.as_view(), name="User Profile"),


# path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

# path('generate-verification-otp', GenerateEmailOTPView.as_view(),
# name='generate-verification-otp'),

# path('verify-email', VerifyOTPView.as_view(), name='verify_email'),
# path('get-all-users', AllUsersView.as_view(), name='verify_email'),
