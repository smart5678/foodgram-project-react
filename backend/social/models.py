from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Follow(models.Model):
    """
    user — ссылка на объект пользователя, который подписывается.
    author — ссылка на объект пользователя, на которого подписываются,
    """
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="subscribed",
        verbose_name="Подписчик"
    )

    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"Редактирование подписки {self.user} на автора {self.author}"
