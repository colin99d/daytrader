from .views import current_user, UserList, update_user_algo, update_user_email, change_password
from django.urls import path

app_name= 'user'
urlpatterns = [
    path('change_password/<str:token>/', change_password, name="change_password"),
    path('current_user/', current_user),
    path('update_algo/', update_user_algo),
    path('update_email/', update_user_email),
    path('users/', UserList.as_view())
]