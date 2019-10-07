from functools import reduce

from django.db.models import Q


class SearchQuerySetMixin:
    """Mixin to add a searches method to a custom QuerySet."""

    def search(self, query):
        """Search action in housings."""
        try:
            fields = self.model.SEARCH_FIELDS
        except AttributeError:
            fields = []
        conditions = [Q(**{f"{field}__icontains": query}) for field in fields]
        if conditions:
            return self.filter(reduce(lambda x, y: x | y, conditions))
        return self.none()
