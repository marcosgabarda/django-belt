# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import random
import string


def random_string(length=16):
    """ Generates a random alphanumeric string.

    :param length: Length of the generated string.
    """
    chars = string.digits + string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))


def random_pin(length=4):
    """ Generates a random numeric string

    :param length: Length of the generated string.
    """
    chars = string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def unique_random_string(model, field, length=16):
    """ Generates a random alphanumeric string, unique in code field from a django class model

    :param length: Length of the generated string.
    :param model: Model class, it has a code field.
    :param field: field name to be sure is unique.
    """
    value = random_string(length)
    while model.objects.filter(**{field: value}).exists():
        length += random.choice([-1, 1])
        value = random_string(length)
    return value
