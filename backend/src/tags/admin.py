from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Управление тегами."""
    list_display = ('id', 'name', 'color', 'slug')
    list_display_links = ('name',)
    list_filter = search_fields = ('name', 'color')
    prepopulated_fields = {'slug': ('name',)}
