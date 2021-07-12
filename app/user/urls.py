from .views import current_user, UserList, update_user_algo
from django.urls import path


urlpatterns = [
    path('current_user/', current_user),
    path('update_user/', update_user_algo),
    path('users/', UserList.as_view())
]