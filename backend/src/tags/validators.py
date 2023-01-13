from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator(validators.RegexValidator):
    """Проверка Названия тега на валидность."""
    regex = r"^[а-яА-ЯёЁa-zA-Z0-9]+$"
    message = "Недопустимый формат Названия тега!"
    flag = 0


@deconstructible
class ColorValidator(validators.RegexValidator):
    """Проверка HEX-кода цвета на валидность."""
    regex = r"^#([A-Fa-f0-9]{3,6})$"
    message = "Недопустимый формат HEX-кода цвета!"
    flag = 0


@deconstructible
class SlugValidator(validators.RegexValidator):
    """Проверка Slug на валидность."""
    regex = r"^[-a-zA-Z0-9_]+$"
    message = "Недопустимый формат Slug-a!"
    flags = 0
