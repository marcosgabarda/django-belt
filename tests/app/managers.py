from django.db import models

from belt.managers import SearchQuerySetMixin
from django.db.models import Count


class PostQuerySet(SearchQuerySetMixin, models.QuerySet):
    pass


class CategoryQuerySet(SearchQuerySetMixin, models.QuerySet):
    pass


class BlogQuerySet(SearchQuerySetMixin, models.QuerySet):
    def annotate_total_posts(self):
        return self.annotate(total_posts=Count("posts"))
