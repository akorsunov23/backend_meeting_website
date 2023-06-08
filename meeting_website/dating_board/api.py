from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from dating_board.serializers import UserListSerializer
from meeting_website.settings import DEFAULT_FROM_EMAIL
from users.models import User


class UsersListAPIView(LoginRequiredMixin, generics.ListAPIView):
    """
    Список всех пользователей с фильтрами и поиском.
    Доступен только аутентифицированным пользователям.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'first_name', 'last_name']


class LikeUserAPIView(GenericAPIView):
    """
    Оценка пользователей.
    Если объявится взаимная симпатия, пользователю отправившему оценку в ответ приходит почта.
    А также на почту обоих пользователей отправляется письмо о взаимной симпатии.
    """
    @staticmethod
    def get(request, pk):
        user = request.user
        user_like = get_object_or_404(User, pk=pk)

        if user_like in user.like.all():
            user.like.remove(user_like)

        else:
            user.like.add(user_like)
            if user in user_like.like.all():
                # если есть взаимная симпатия отправляем обоим пользователям сообщение на почту

                message_to_user = f'Почта пользователя - {user_like.email}'
                send_mail(
                    subject=f'Вам понравился пользователь',
                    message=message_to_user,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email, ]
                )

                message_to_uses_like = f'У Вас взаимная симпатия с {user.first_name} {user.last_name}.\n' \
                                       f'Его почта - {user.email}.'
                send_mail(
                    subject=f'Вы понравились на сайте знакомств',
                    message=message_to_uses_like,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[user_like.email, ])

                return Response(
                    {
                        'email_like_user': user_like.email
                    },
                    status=status.HTTP_200_OK
                )

        return Response(status=status.HTTP_200_OK)
