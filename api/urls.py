from django.urls import path

from api.views.all_users import AllUsersView
from api.views.create_user import CreateUsersView
from api.views.sign_in import SignInView

urlpatterns = [
    path("all-users", AllUsersView.as_view(), name="All-Users"),
    path("create-users", CreateUsersView.as_view(), name="Create-Users"),
    path("sign-in", SignInView.as_view(), name="sign-in"),
]
# path('login', UserLoginView.as_view(), name="User Login"),
# path('profile', UserProfileView.as_view(), name="User Profile"),
# path('change_password', UserChangePasswordView.as_view(), name="Change User Password"),

# path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),
# name='send-reset-password-email'),


# path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

# path('generate-verification-otp', GenerateEmailOTPView.as_view(),
# name='generate-verification-otp'),

# path('verify-email', VerifyOTPView.as_view(), name='verify_email'),
# path('get-all-users', AllUsersView.as_view(), name='verify_email'),
