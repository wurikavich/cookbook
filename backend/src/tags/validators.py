from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class ColorValidator(validators.RegexValidator):
    regex = r"^#([A-Fa-f0-9]{3,6})$"
    message = "Hex кода цвета!"
    flag = 0


@deconstructible
class NameValidator(validators.RegexValidator):
    regex = r"^[а-яА-ЯёЁa-zA-Z0-9]+$"
    message = "Неверный формат названия тега!"
    flag = 0


@deconstructible
class SlugValidator(validators.RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = "Неверный формат слага!"
    flags = 0
