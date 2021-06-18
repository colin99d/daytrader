from .views import home, table
from django.urls import path


urlpatterns = [
    path('', home, name="home"),
    path('table', table, name="table")
]