from user.views import CustomAuthToken
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('backend/api/password_reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
    path('backend/api-token-auth/', CustomAuthToken.as_view(),
         name='api_token_auth'),
    path('backend/admin/', admin.site.urls),
    path('backend/', include('trader.urls')),
    path('backend/user/', include('user.urls', namespace='user')),
    path('backend/', include('chat.urls'))
]
