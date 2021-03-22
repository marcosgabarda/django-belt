from functools import reduce
from typing import TYPE_CHECKING, Dict, List, Sequence, Tuple, Union

from django.db.models import CharField, Q, Value
from django.db.models.functions import Concat

if TYPE_CHECKING:
    from django.db.models import QuerySet


class SearchQuerySetMixin:
    """Mixin to add a searches method to a custom QuerySet."""

    def search(self, query: str) -> "QuerySet":
        """Search over the fields defined in the model."""
        if not query:
            return self  # Ignore the search if it's an empty sting
        try:
            fields: List[
                Union[Tuple[str, str], str]
            ] = self.model.SEARCH_FIELDS  # type: ignore
        except AttributeError:
            fields = []
        try:
            combined_fields: Dict[str, Sequence] = self.model.SEARCH_COMBINED_FIELDS  # type: ignore
        except AttributeError:
            combined_fields = {}
        conditions: List = []
        queryset: "QuerySet" = self
        if combined_fields:
            annotations = {}
            for name, combined_field in combined_fields.items():
                concat = []
                for item in combined_field:
                    concat += [item, Value(" ")]
                print(concat)
                annotations[name] = Concat(*concat, output_field=CharField())
            queryset = self.annotate(**annotations)  # type: ignore
        conditions += [
            Q(**{f"{field}__icontains": query})
            for field in fields + list(combined_fields.keys())
        ]
        if conditions:
            return queryset.filter(reduce(lambda x, y: x | y, conditions)).distinct()
        return self.none()  # type: ignore
