import random

from django.utils.crypto import get_random_string


def unique_model_random_string(
    model,
    field,
    length=16,
    allowed_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
):
    """Generates a random alphanumeric string, unique in code field from a django
    class model

    :param length: Length of the generated string.
    :param model: Model class, it has a code field.
    :param field: field name to be sure is unique.
    :param allowed_chars: allowed chars to select.
    """
    value = get_random_string(length, allowed_chars=allowed_chars)
    while model.objects.filter(**{field: value}).exists():
        length += random.choice([-1, 1])
        value = get_random_string(length, allowed_chars=allowed_chars)
    return value
