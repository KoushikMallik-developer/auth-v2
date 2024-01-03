from django.urls import path

from api.views.seller_views.create_seller import CreateSellerView
from api.views.seller_views.seller_details import SellerDetailView
from api.views.seller_views.sign_in import SellerSignInView
from api.views.seller_views.update_seller_details import UpdateSellerProfileView
from api.views.user_views.add_delivery_address import AddDeliveryAddress
from api.views.all_users import AllUsersView
from api.views.clear_server_cache import ClearServerCaches
from api.views.user_views.create_user import CreateUsersView
from api.views.common_views.otp_view import SendOTPView
from api.views.common_views.password_reset import PasswordResetView
from api.views.common_views.remove_user import RemoveUserView
from api.views.user_views.sign_in import SignInView
from api.views.user_views.update_delivery_address import UpdateDeliveryAddress
from api.views.common_views.update_password import UpdatePasswordView
from api.views.user_views.update_profile import UpdateProfileView
from api.views.user_views.user_details import UserDetailView
from api.views.common_views.validate_otp_view import ValidateOTPView

urlpatterns = [
    # User Paths
    path("create-users", CreateUsersView.as_view(), name="Create-Users"),
    path("sign-in", SignInView.as_view(), name="user-sign-in"),
    path("update-profile", UpdateProfileView.as_view(), name="Update-User-profile"),
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
    # Seller Paths
    path("seller/create-users", CreateSellerView.as_view(), name="Seller-Create-Users"),
    path("seller/sign-in", SellerSignInView.as_view(), name="seller-sign-in"),
    path(
        "seller/update-profile",
        UpdateSellerProfileView.as_view(),
        name="seller-sign-in",
    ),
    path("seller/seller-details", SellerDetailView.as_view(), name="seller-details"),
    # General Paths
    path("all-users", AllUsersView.as_view(), name="All-Users"),
    path("remove-user", RemoveUserView.as_view(), name="Remove-User"),
    path("send-otp", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp", ValidateOTPView.as_view(), name="verify-otp"),
    path(
        "reset-password",
        PasswordResetView.as_view(),
        name="send-reset-password-email",
    ),
    path("update-password", UpdatePasswordView.as_view(), name="Change-User-Password"),
    path("clear-caches", ClearServerCaches.as_view(), name="clear-caches"),
]
