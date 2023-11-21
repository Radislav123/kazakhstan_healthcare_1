import os

from django.core.exceptions import ValidationError


def validate_path(value: str) -> None:
    if not os.path.isabs(value):
        raise ValidationError("%(value)s не выглядит как абсолютный путь", params = {"value": value})
