from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    class Meta:
        model = User
        fields = [
            'id', 'photo', 'gender', 'username',
            'first_name', 'last_name', 'email', 'password',
            'longitude', 'latitude',
        ]
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    """Класс Serializer для аутентификации пользователей по email и паролю."""
    email = serializers.CharField(max_length=255, write_only=True, label='Электронная почта')
    password = serializers.CharField(max_length=128, write_only=True, label='Пароль')

    def validate(self, data):
        """Проверка существование пользователя."""
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError('Пользователь не найден, проверьте введённые данные')
        if not user.is_active:
            raise serializers.ValidationError('Пользователь неактивен')
        return user
