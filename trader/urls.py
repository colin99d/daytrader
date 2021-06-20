from .views import home, table, StockView, DecisionView
from rest_framework import routers

from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'stocks', StockView, 'stocks')
router.register(r'decisions', DecisionView, 'decisions')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home, name="home"),
    path('table', table, name="table")
]