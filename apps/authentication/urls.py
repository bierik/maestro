from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from apps.authentication.views import LogoutView, UserView

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
]
