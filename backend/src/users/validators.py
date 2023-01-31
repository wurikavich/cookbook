import re

from django.conf import settings
from django.core.exceptions import ValidationError


def user_validate_name(value):
    """Проверка на наличие запрещенных символов в имени пользователей."""
    if match := re.findall(r"[0123456789$%^&#=+:<>_;!()]", value):
        raise ValidationError(f'Запрещенный символ {match}')


def validate_prohibited_name(value):
    """Проверка запрещенных имен."""
    if value.lower() in settings.FORBIDDEN_NAMES:
        raise ValidationError(f"Использовать '{value}' запрещено!")
