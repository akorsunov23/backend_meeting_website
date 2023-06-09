from django.urls import path

from dating_board.api import UsersListAPIView, LikeUserAPIView

app_name = 'dating_board'

urlpatterns = [
    path('list_users/', UsersListAPIView.as_view(), name='user_list'),
    path('like_user/<int:pk>/', LikeUserAPIView.as_view(), name='user_like'),
]
