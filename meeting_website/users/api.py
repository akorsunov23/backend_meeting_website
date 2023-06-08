from rest_framework import generics

from .models import User
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Представление регистрации нового пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
