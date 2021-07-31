from django.urls import include, path
from rest_framework.routers import DefaultRouter

from social.views import SubscriptionsViewSet

# router = DefaultRouter()
#
# router.register(
#     r'user',
#     UserViewSet,
#     basename='user'
# )

urlpatterns = [
    path('users/subscriptions/', SubscriptionsViewSet, name='subscriptions'),
]