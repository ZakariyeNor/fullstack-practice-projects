from django.urls import path
from .views import register, profile, change_password, delete_account
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", profile, name="profile"),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password.html",
            success_url="/"
        ),
        name="change_password"
    ),
    path("delete-account/", delete_account, name="delete_account"),
]
