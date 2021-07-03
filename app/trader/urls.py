from .views import home, cashflows, StockView, DecisionView, AlgorithmView
from rest_framework import routers

from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'stocks', StockView, basename='stocks')
router.register(r'decisions', DecisionView, basename='decisions')
router.register(r'algorithms', AlgorithmView, basename='algorithms')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home, name="home"),
    path('cashflows/', cashflows, name="cashflows")
]