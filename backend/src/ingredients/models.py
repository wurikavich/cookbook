from django.conf import settings
from django.db import models

from src.base.validators import recipe_validate_name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPE_FIELD,
        unique=True,
        db_index=True,
        verbose_name="Наименование ингредиента",
        help_text="Добавьте ингредиент",
        validators=(recipe_validate_name,)
    )
    measurement_unit = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPE_FIELD,
        verbose_name="Единица измерения",
        help_text="Выберите единицу измерения"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"
