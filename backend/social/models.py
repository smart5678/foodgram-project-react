from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

USER = get_user_model()


class Follow(models.Model):
    """
    user — ссылка на объект пользователя, который подписывается.
    author — ссылка на объект пользователя, на которого подписываются,
    """
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='user-author'
        ), ]

    def __str__(self):
        return (f'Пользователь {self.user}'
                f' подписан на автора рецепта {self.author}')


class Favorite(models.Model):
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [models.UniqueConstraint(
            fields=['user', 'favorite_recipe'],
            name='user-favorite_recipe'
        ), ]
