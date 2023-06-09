from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import geodesic
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
    Реализована фильтрация по имени, фамилии, пола и дистанции.
    """
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'first_name', 'last_name']

    def get_queryset(self):
        """Фильтрация по дистанции."""
        queryset = User.objects.exclude(pk=self.request.user.pk)

        if self.request.query_params.get('distance'):
            # заданная дистанция
            distance = self.request.query_params.get('distance')
            # координаты запросившего пользователя
            user_coordinates = (self.request.user.latitude, self.request.user.longitude)
            result = list()
            for user_filter in queryset:
                # координаты фильтруемого пользователя из БД
                user_filter_coordinates = (user_filter.latitude, user_filter.longitude)
                # геодезическое расстояние между точками
                estimated_distance = geodesic(user_coordinates, user_filter_coordinates)
                # если в пределах заданной дистанции, добавляем в результат
                if estimated_distance <= float(distance):
                    result.append(user_filter.pk)
            # возвращаем отфильтрованный queryset
            return queryset.filter(pk__in=result)

        return queryset


class LikeUserAPIView(LoginRequiredMixin, GenericAPIView):
    """
    Оценка пользователей.
    Если объявится взаимная симпатия, пользователю отправившему оценку в ответ приходит почта.
    А также на почту обоих пользователей отправляется письмо о взаимной симпатии.
    Доступен только аутентифицированным пользователям.
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
                    subject='Вам понравился пользователь',
                    message=message_to_user,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email, ]
                )

                message_to_uses_like = f'У Вас взаимная симпатия с {user.first_name} {user.last_name}.\n' \
                                       f'Его почта - {user.email}.'
                send_mail(
                    subject='Вы понравились на сайте знакомств',
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
