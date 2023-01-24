from django.conf import settings
from django.db import models

from src.tags.validators import ColorValidator, NameValidator, SlugValidator


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_TAG_MODEL_FIELD,
        unique=True,
        verbose_name="Название",
        help_text="Введите тег",
        validators=(NameValidator(),)
    )
    color = models.CharField(
        max_length=settings.MAX_LENGTH_TAG_COLOR,
        unique=True,
        verbose_name="HEX-код цвета",
        help_text="Добавьте цвет в формате HEX-кода",
        validators=(ColorValidator(),)
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_TAG_MODEL_FIELD,
        unique=True,
        verbose_name="Slug",
        help_text="Добавьте slug",
        validators=(SlugValidator(),)
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
