from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей."""
    like = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'photo', 'gender',
            'first_name', 'last_name',
            'longitude', 'latitude',
            'like',
        ]

    @staticmethod
    def get_like(obj):
        user = User.objects.prefetch_related('likes').get(id=obj.id)
        num_likes_received = user.likes.count()
        return num_likes_received
