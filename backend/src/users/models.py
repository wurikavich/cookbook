from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from src.users.validators import user_validate_name, validate_prohibited_name


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    username = models.CharField(
        max_length=settings.MAX_LENGTH_USER_MODEL_FIELD,
        unique=True,
        verbose_name="Логин",
        help_text="Придумайте уникальный логин",
        validators=[UnicodeUsernameValidator(),
                    validate_prohibited_name]
    )
    email = models.EmailField(
        max_length=settings.MAX_LENGTH_USER_EMAIL,
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Введите адрес электронной почты, необходим для авторизации"
    )
    first_name = models.CharField(
        max_length=settings.MAX_LENGTH_USER_MODEL_FIELD,
        validators=[user_validate_name],
        verbose_name="Имя",
        help_text="Введите своё имя"
    )
    last_name = models.CharField(
        max_length=settings.MAX_LENGTH_USER_MODEL_FIELD,
        validators=[user_validate_name],
        verbose_name="Фамилия",
        help_text="Введите свою фамилию"
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок пользователей."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="+"
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='exclude a new subscription when it is valid',
                fields=['user', 'author']),
            models.CheckConstraint(
                name='disable subscribe to yourself',
                check=~models.Q(user=models.F('author')))
        ]

    def __str__(self):
        return (f'"{self.user}" с "id:{self.user.id}" подписался '
                f'на автора "{self.author}" c "id:{self.author.id}"')
