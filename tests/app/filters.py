import django_filters

from belt.django_filters.filters import SearchFilter
from tests.app.models import Post


class PostFilter(django_filters.rest_framework.FilterSet):
    search = SearchFilter()

    class Meta:
        model = Post
        fields = ["search", "status"]
