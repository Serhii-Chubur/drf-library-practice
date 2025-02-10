from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUser, ManageUser

urlpatterns = [
    path("register/", CreateUser.as_view(), name="register"),
    path("me/", ManageUser.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
