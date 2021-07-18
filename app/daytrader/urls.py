"""daytrader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from rest_framework.authtoken.views import obtain_auth_token
from user.views import CustomAuthToken
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('backend/api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('backend/api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('backend/admin/', admin.site.urls),
    path('backend/',include('trader.urls')),
    path('backend/user/', include('user.urls', namespace='user')),
    path('backend/', include('chat.urls'))
]
