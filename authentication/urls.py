from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from authentication.views import LogoutView
from authentication.views import UserView

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
]
