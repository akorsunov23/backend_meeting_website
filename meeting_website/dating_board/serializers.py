from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей."""
    like = serializers.IntegerField(source='like.count')
    # distance = serializers.DecimalField(decimal_places=0, max_digits=2)

    class Meta:
        model = User
        fields = [
            'photo', 'gender',
            'first_name', 'last_name',
            'longitude', 'latitude',
            'like'
        ]
