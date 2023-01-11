from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from .validators import recipe_validate_name
from ..tags.models import Tag
from ..users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPE_FIELD,
        unique=True,
        validators=[recipe_validate_name],
        verbose_name="Наименование ингредиента",
        help_text="Добавьте ингредиент"
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


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPE_FIELD,
        validators=[recipe_validate_name],
        verbose_name="Название",
        help_text="Введите название рецепта"
    )
    text = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание рецепта"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        help_text="Укажите время приготовления, мин",
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Время приготовления не может быть меньше 1 минуты!")]
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
        help_text="Выберите автора рецепта"
    )
    image = models.ImageField(
        verbose_name="Изображение",
        help_text="Добавьте изображение",
        upload_to="recipes_images/%Y/%m/%d/"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='+',
        verbose_name="Теги",
        help_text="Выберите теги"
    )
    ingredients = models.ManyToManyField(
        "IngredientRecipe",
        symmetrical=False,
        related_name='+',
        verbose_name="Ингредиенты",
        help_text="Выберите ингредиенты"
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Вспомогательная модель для создания рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Рецепт",
        help_text="Выберите рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name="Ингредиент",
        help_text="Выберите ингредиент"
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        help_text="Укажите необходимое количество ингредиента",
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Количество ингредиента не может быть меньше 1")]
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


class Favourite(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name='+'
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                name='exclude the addition to favorites, if present',
                fields=['user', 'recipe'])
        ]

    def __str__(self):
        return f'"{self.user}" добавил в избранное рецепт "{self.recipe}".'


class Purchases(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Пользователь"

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Рецепт"
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                name='exclude the addition to shopping list,if present',
                fields=['user', 'recipe'])
        ]

    def __str__(self):
        return f'"{self.user}" добавил в список покупок рецепт "{self.recipe}"'
