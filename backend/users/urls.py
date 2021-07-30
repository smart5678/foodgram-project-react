from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, SubscriptionsViewSet

router = DefaultRouter()

router.register(
    r'user',
    UserViewSet,
    basename='user'
)

urlpatterns = [
    path('users/subscriptions/', SubscriptionsViewSet, name='subscriptions'),
    path('/users/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]