from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Вывод информации о теге."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
