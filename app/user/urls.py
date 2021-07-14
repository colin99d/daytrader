from .views import current_user, UserList, update_user_algo, update_user_email
from django.urls import path


urlpatterns = [
    path('current_user/', current_user),
    path('update_algo/', update_user_algo),
    path('update_email/', update_user_email),
    path('users/', UserList.as_view())
]