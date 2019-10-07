from django.db import models

from belt.managers import SearchQuerySetMixin


class PostQuerySet(SearchQuerySetMixin, models.QuerySet):
    pass


class CategoryQuerySet(SearchQuerySetMixin, models.QuerySet):
    pass
