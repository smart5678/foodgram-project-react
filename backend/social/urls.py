from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from social.views import SubscriptionsViewSet

router = DefaultRouter()

router.register(
    r'',
    SubscriptionsViewSet,
    basename='subscriptions'
)

urlpatterns = [
    url('', include(router.urls)),
]