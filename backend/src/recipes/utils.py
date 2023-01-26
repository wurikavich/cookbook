import io
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from config import settings
from src.base.serializers import RecipeShortInfoSerializer
from src.recipes.models import Recipe, UserRecipeRelation
from src.recipes.serializers import UserRecipeRelationSerializer


def create_or_delete(request, pk, source):
    """Сохранение/удаление рецепта в избранное или список покупок."""

    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user
    if request.method == 'POST':
        serializer = UserRecipeRelationSerializer(
            data={'user': user.id, 'recipe': recipe.id, source: True},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        obj, _ = UserRecipeRelation.objects.get_or_create(
            user=user, recipe=recipe
        )
        if source == 'favourites':
            obj.favourites = True
        elif source == 'purchases':
            obj.purchases = True
        obj.save()
        serializer = RecipeShortInfoSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    obj = get_object_or_404(UserRecipeRelation, user=user, recipe__id=pk)
    if source == 'favourites':
        obj.favourites = False
    elif source == 'purchases':
        obj.purchases = False
    obj.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


def create_pdf_file(shopping_list):
    """Сформировать из входящих данных pdf-файл с необходимы ингредиентами."""
    times_location = settings.STATIC_ROOT + '/fonts/times.ttf'
    times_name = 'Times'
    current_date = datetime.today().strftime("%d.%m.%Y")

    pdfmetrics.registerFont(TTFont(times_name, times_location, 'UTF-8'))

    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)

    page.setFont(times_name, size=18)
    page.drawString(120, 800, f'Список покупок на {current_date}:')
    page.setFont(times_name, size=16)
    height = 750
    for number, ing in enumerate(shopping_list, 1):
        string = f'{number}. {ing[0]} - {ing[2]}, {ing[1]}'
        page.drawString(40, height, string)
        height -= 25
    page.showPage()
    page.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename='Список_покупок.pdf')
