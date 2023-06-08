from django.urls import path

from users.api import CreateUserView

app_name = 'users'


urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    # path('api/clients/<int:id>/match/', MatchCreateView.as_view(), name='create_match'),
    # path('api/list/', UserListView.as_view(), name='user_list'),
    # path('api/list/distance/', UserDistanceFilterView.as_view(), name='user_distance_list'),
]
