import re

from django.core.exceptions import ValidationError


def recipe_validate_name(value):
    """Проверка на наличие запрещенных символов в имени пользователей."""
    if match := re.findall(r"[$^#:;!?]", value):
        raise ValidationError(f'Запрещенный символ {match}')
