import io

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from ..recipes.models import Recipe
from ..users.serializers import RecipeShortSerializer


def get_boolean_value(self, obj, method):
    """Возвращает логическое значение для полей сериализатора."""
    request = self.context.get('request')
    if not request or request.user.is_anonymous:
        return False
    current_user = {
        'get_is_favorited': request.user.favorites,
        'get_is_in_shopping_cart': request.user.purchases
    }
    return current_user[method].filter(recipe=obj).exists()


def get_queryset(queryset, value, user):
    """Возвращает queryset, который используют фильтры."""
    if value:
        return queryset.filter(id__in=user.values_list('recipe', flat=True))
    return queryset


def add_object(models, user, pk):
    """Создание объекта модели."""
    if models.objects.filter(user=user, recipe__id=pk).exists():
        return Response({'error': 'Запись уже добавлена!'},
                        status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, pk=pk)
    models.objects.create(user=user, recipe=recipe)
    serializer = RecipeShortSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_object(models, user, pk):
    """Удаление объекта модели."""
    obj = get_object_or_404(models, user=user, recipe_id=pk)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def create_pdf_file(shopping_list):
    """Сформировать из входящих данных pdf-файл с необходимы ингредиентами."""
    sans_regular = settings.STATIC_ROOT + '/fonts/OpenSans-Regular.ttf'
    sans_regular_name = 'OpenSans-Regular'

    pdfmetrics.registerFont(TTFont(sans_regular_name, sans_regular))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont(sans_regular_name, 20)
    c.drawString(30, 800, 'Список продуктов:')

    val = 765
    for key, value in shopping_list.items():
        string = f'• {key} - {value[0]} {value[1]}'
        c.drawString(30, val, string)
        val -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='shopping_list.pdf'
    )
