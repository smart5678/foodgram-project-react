from django.contrib.auth import get_user_model
from django.db import models


from recipes.models import Recipe

USER = get_user_model()


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchased',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='purchased-buyer'
        ), ]

    def __str__(self):
        return self._meta.verbose_name
