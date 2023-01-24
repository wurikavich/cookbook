from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from src.base.validators import recipe_validate_name
from src.ingredients.models import Ingredient
from src.tags.models import Tag
from src.users.models import User


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPE_FIELD,
        verbose_name="Название",
        help_text="Введите название рецепта",
        validators=(recipe_validate_name,)
    )
    text = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание рецепта"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
        help_text="Выберите автора рецепта"
    )
    readers = models.ManyToManyField(
        User,
        through="UserRecipeRelation",
        related_name="read_recipes",
        verbose_name="Рецепты сохраненные у пользователей"
    )
    image = models.ImageField(
        verbose_name="Изображение",
        help_text="Добавьте изображение",
        upload_to="recipes_images/%Y/%m/%d/"
    )
    tags = models.ManyToManyField(
        Tag,
        symmetrical=False,
        related_name="+",
        verbose_name="Теги"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        related_name="recipes",
        verbose_name="Ингредиенты",
        help_text="Выберите ингредиенты"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        help_text="Укажите время приготовления, мин",
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Время приготовления не может быть меньше 1 минуты!")
        ]
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Вспомогательная модель. Сохраняет количество ингредиентов в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="amounts",
        verbose_name="Рецепт",
        help_text="Выберите рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Ингредиент",
        help_text="Выберите ингредиент"
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        help_text="Укажите необходимое количество ингредиента",
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Количество ингредиента не может быть меньше 1")
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецептах'
        constraints = [
            models.UniqueConstraint(
                name='exclude the addition of an ingredient if present',
                fields=['ingredient', 'recipe'])
        ]

    def __str__(self):
        return (f'Количество "{self.ingredient}" в рецепте "{self.recipe}" -'
                f' {self.amount} {self.ingredient.measurement_unit}.')


class UserRecipeRelation(models.Model):
    """Рецепты добавленные пользователями в избранное и список покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="readers_user",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="readers_recipe",
        verbose_name="Рецепт"
    )
    favourites = models.BooleanField(
        default=False,
        verbose_name="В избранном",
        help_text="Находится ли рецепт в избранном у пользователя"
    )
    purchases = models.BooleanField(
        default=False,
        verbose_name="В списке покупок",
        help_text="Находится ли рецепт в списке покупок у пользователя"
    )

    class Meta:
        verbose_name = 'Рецепты сохраненные у пользователя'
        verbose_name_plural = 'Рецепты сохраненные у пользователей'
        constraints = [
            models.UniqueConstraint(
                name='exclude the addition, if present',
                fields=['user', 'recipe'])
        ]

    def __str__(self):
        return f'"{self.user}" добавил рецепт "{self.recipe}".'
