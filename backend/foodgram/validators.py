import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if re.search(r'^[\w.@+-]+$', value) is None:
        raise ValidationError(
            ('Допустимы буквы латинского алфавита, цифры и символы .@+-'),
            params={'value': value},
        )


def validate_slug(value):
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            ('Допустимы буквы латинского алфавита, цифры и символы _-'),
            params={'value': value},
        )
