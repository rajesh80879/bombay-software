from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path("register/", register_user, name="register"),
    path("", login_user, name="login"),
    path("login_data/", login_data, name="logindata"),
    path("users/",users,name="users"),
    path("fp-email/", forgot, name="fp-email"),
    path("fp-email-page", fpEmailPage, name="forgotemailpage"),
    path("forgot-email/", femail, name="forgotemail"),
    path("fp-otp-page", fpOTPPage, name="forgototppage"),
    path("profile/", profile, name="profile"),
    path("fp-password-page", fpPasswordPage, name="forgotpasswordpage"),
    path("fp-password-data", fpPasswordData, name="forgotpassworddata"),
    path("fpotp/", fpOTP, name="forgototp"),
    path("badrequest/", bad_Request, name="badrequest"),
    path("updateuser", update_user, name="update-user"),
    path("show-user/<int:id>", show_user, name="show-user"),
    path("logout/", logout_user, name="logout-user"),
    path('change-password/', changePassword, name="change-password")

    ]