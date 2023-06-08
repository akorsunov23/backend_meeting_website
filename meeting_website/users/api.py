from django.contrib.auth import login, logout
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, UserLoginSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """Представление регистрации нового пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginAPIView(GenericAPIView):
    """Аутентификация существующего пользователя."""
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response(
            data={
                'response': f'{request.data["email"]} аутентифицирован.'
            },
            status=status.HTTP_200_OK
        )


class UserLogoutAPIView(GenericAPIView):
    """Выход пользователя."""
    @staticmethod
    def get(request):
        logout(request)
        return Response(
            data={
                'response': 'Вы вышли из аккаунта.'
            },
            status=status.HTTP_200_OK
        )
