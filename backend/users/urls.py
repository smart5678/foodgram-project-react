from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import login

router = DefaultRouter()
# router.register('', UsersViewSet)

urlpatterns = [
    path('token/login/', login),
    # path('v1/auth/email/', request_code),

]