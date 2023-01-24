from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

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
    pdfmetrics.registerFont(TTFont('Times', 'times.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="Список_покупок.pdf"')
    page = canvas.Canvas(response)
    page.setFont('Times', size=20)
    page.drawString(
        120, 800,
        f'Список покупок на {datetime.today().strftime("%d.%m.%Y")}.')
    page.setFont('Times', size=15)
    height = 750
    for number, ingredient in enumerate(shopping_list, 1):
        page.drawString(40, height, (
            f'{number}. {ingredient[0]} - {ingredient[2]}, {ingredient[1]}'))
        height -= 25
    page.showPage()
    page.save()
    return response
