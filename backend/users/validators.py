import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if re.search(r'^[\w.@+-]+$', value) is None:
        raise ValidationError(
            ('Допустимы буквы латинского алфавита, цифры и символы .@+-'),
            params={'value': value},
        )
