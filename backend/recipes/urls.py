from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

router = DefaultRouter()

router.register(
    r'',
    RecipeViewSet,
    basename='TitleView'
)
# router.register(
#     'genres',
#     GenreViewSet,
#     basename='GenreView'
# )
# router.register(
#     'categories',
#     CategoryViewSet,
#     basename='CategoryView'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews')

urlpatterns = [
    path('/', include(router.urls)),
]
