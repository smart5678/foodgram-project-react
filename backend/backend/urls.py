#import debug_toolbar
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api', include('recipes.urls')),
]
urlpatterns += [url('api/', include('users.urls'))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]