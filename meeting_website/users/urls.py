from django.urls import path

from users.api import \
    CreateUserAPIView, \
    UserLoginAPIView, \
    UserLogoutAPIView

app_name = 'users'


urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='create_user'),
    path('login/', UserLoginAPIView.as_view(), name='login_user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout_user'),
]
