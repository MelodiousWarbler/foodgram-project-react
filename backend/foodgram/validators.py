import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if re.search(r'^[\w.@+-]+\z', value) is None:
        raise ValidationError(
            ('Допустимы значения по маске ^[\w.@+-]+\z'),
            params={'value': value},
        )


def validate_slug(value):
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            ('Допустимы значения по маске ^[-a-zA-Z0-9_]+$'),
            params={'value': value},
        )
