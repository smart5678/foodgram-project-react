from django.forms import ModelForm

from recipes.models import Recipe


class CustomRecipeForm(ModelForm):
    """
    Форма редактирования пользователя в админпанели
    """
    class Meta:
        model = Recipe
        fields = (
            'name', 'author',
            'tags',
            'image',
            'cooking_time',
            'text',
            'favorite_count'
        )
        readonly_fields = ['created_at']


