from django.db.models.constants import LOOKUP_SEP
from django_filters import CharFilter
from rest_framework import filters


class SearchFilter(CharFilter):
    """Filter to use searches QuerySet method."""

    def filter(self, qs, value):
        if hasattr(qs, "search"):
            return qs.search(query=value)
        return qs


class UnaccentSearchFilter(filters.SearchFilter):
    """
    https://docs.djangoproject.com/en/3.1/ref/contrib/postgres/lookups/#unaccent
    You need migrate the postgres database and add 'django.contrib.postgres' in your INSTALLED_APPS
    ./manage.py makemigrations myapp --empty

    from django.contrib.postgres.operations import UnaccentExtension
    class Migration(migrations.Migration):
        operations = [
            UnaccentExtension()
        ]
    """

    def construct_search(self, field_name):
        lookup = "unaccent__icontains"
        return LOOKUP_SEP.join([field_name, lookup])
