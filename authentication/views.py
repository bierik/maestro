from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import UserSerializer


class LogoutView(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response()


class UserView(APIView):
    def get(self, request):
        user = UserSerializer(request.user).data
        return Response(data={"user": user})
