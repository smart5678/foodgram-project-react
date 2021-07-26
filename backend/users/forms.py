from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Форма создания пользователя в админпанели
    """
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'role', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """
    Форма редактирования пользователя в админпанели
    """
    class Meta:
        model = User
        fields = ('email', 'role', 'first_name', 'last_name')
