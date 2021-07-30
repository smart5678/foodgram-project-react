from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Дополненная модель пользователя наследник AbstractBaseUser
    Добавлены поля role: admin, user
    email, username - уникальные, username может быть пустым при создании
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', 'admin'
        USER = 'user', 'user'

    role = models.CharField(
        'Уровень доступа',
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    username = models.CharField('Имя пользователя', max_length=150,
                                blank=False, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField('Администраторы', default=False)
    is_active = models.BooleanField('Активен', default=True)
    last_login = models.DateTimeField('last login', blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    password = models.CharField('Пароль', max_length=150, blank=True)
    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_user(self):
        return self.role == self.Role.USER


class Follow(models.Model):
    """
    user — ссылка на объект пользователя, который подписывается.
    author — ссылка на объект пользователя, на которого подписываются,
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribed",
        verbose_name="Подписчик"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"Редактирование подписки {self.user} на автора {self.author}"