from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet, IngredientViewSet

router = DefaultRouter()

router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
router.register(
    'tags',
    TagViewSet,
    basename='TagView'
)
router.register(
    'ingredients',
    IngredientViewSet,
    basename='CategoryView'
)
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
