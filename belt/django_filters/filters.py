from django_filters import CharFilter


class SearchFilter(CharFilter):
    """Filter to use searches QuerySet method."""

    def filter(self, qs, value):
        if hasattr(qs, "search"):
            return qs.search(query=value)
        return qs
