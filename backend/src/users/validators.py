import re

from django.core.exceptions import ValidationError


def user_validate_name(value):
    if match := re.findall(r"[0123456789$%^&#=+:<>_;!()]", value):
        raise ValidationError(f'Запрещенный символ {match}')


def validate_prohibited_name(value):
    if value.lower() == "me":
        raise ValidationError('Запрещено использовать "me"')
