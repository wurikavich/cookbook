def get_queryset(queryset, value, user):
    """Возвращает queryset, который используют фильтры."""
    if value:
        return queryset.filter(
            id__in=user.values_list('recipe', flat=True))
    return queryset
