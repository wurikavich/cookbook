import io

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from src.base.serializers import RecipeShortInfoSerializer
from src.recipes.models import Recipe


def add_object(models, user, pk):
    """Создание объекта модели."""
    recipe = get_object_or_404(Recipe, pk=pk)
    if models.objects.filter(user=user, recipe__id=pk).exists():
        return Response({'error': 'Запись уже добавлена!'},
                        status=status.HTTP_400_BAD_REQUEST)
    models.objects.create(user=user, recipe=recipe)
    serializer = RecipeShortInfoSerializer(recipe)
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
