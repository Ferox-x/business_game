from django.urls import path

from apps.authenticate.views import (
    LoginAPIView,
    PasswordChangeAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    RefreshAPIView,
    RegistrationAPIView,
    RegistrationCoordinatorAPIView,
    TestView,
)

urlpatterns = [
    path("api/signup/", RegistrationAPIView.as_view(), name="registrate-player"),
    path(
        "api/signup/coordinator",
        RegistrationCoordinatorAPIView.as_view(),
        name="registrate-coordinator",
    ),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("api/refresh/", RefreshAPIView.as_view(), name="api-refresh"),
    path("api/test", TestView.as_view()),
    path("api/reset-password/", PasswordResetAPIView.as_view(), name="password-reset"),
    path(
        "api/reset/<token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="confirm-password-reset",
    ),
    path(
        "api/change-password", PasswordChangeAPIView.as_view(), name="password-change"
    ),
]
