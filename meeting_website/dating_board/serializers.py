from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей."""
    class Meta:
        model = User
        fields = [
            'photo', 'gender',
            'first_name', 'last_name',
            'longitude', 'latitude',
        ]
