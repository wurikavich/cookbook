from django.conf import settings
from django.db import models

from .validators import ColorValidator, NameValidator, SlugValidator


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_TAG_MODEL_FIELD,
        unique=True,
        validators=[NameValidator()],
        verbose_name="Название",
        help_text="Введите тег"
    )
    color = models.CharField(
        max_length=settings.MAX_LENGTH_TAG_COLOR,
        unique=True,
        validators=[ColorValidator()],
        verbose_name="HEX-код цвета",
        help_text="Добавьте цвет в формате HEX-кода"
    )

    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_TAG_MODEL_FIELD,
        unique=True,
        validators=[SlugValidator()],
        verbose_name="Slug",
        help_text="Добавьте slug"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
