from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include('djoser.urls')),
    url(r'^api/auth/', include('djoser.urls.authtoken')),
    url(r'^api/auth/', include('djoser.urls.jwt')),
]
