from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from social.views import SubscriptionsViewSet

router = DefaultRouter()

router.register(
    r'subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)

urlpatterns = [
    url(r'^users/', include(router.urls)),
]