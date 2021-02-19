from typing import Dict, List, Type, Union

from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class ActionSerializersMixin:
    """
    Mixin for ViewSets that allows to have a dict with a serializer for
    each action.
    """

    action_serializers: Dict[str, Type[Serializer]] = {}

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super().get_serializer_class()


class SimpleSerializationMixin:
    """
    Mixin to simplify serialization of object instances.
    """

    def serialize_instance(self, data) -> Union[Dict, List]:
        serializer_class = self.get_serializer_class()  # type: ignore
        serializer = serializer_class(instance=data)

        return serializer.data


class SimplePaginationMixin:
    """
    Mixin to simplify pagination.
    """

    def paginate(self, queryset: QuerySet) -> Response:
        page = self.paginate_queryset(queryset)  # type: ignore
        if page is not None:
            serializer = self.get_serializer(page, many=True)  # type: ignore
            return self.get_paginated_response(serializer.data)  # type: ignore

        serializer = self.get_serializer(queryset, many=True)  # type: ignore
        return Response(serializer.data)


class SimpleValidationMixin:
    """
    Mixin to simplify validation.
    """

    def validate(self, data: dict, raise_exception=True) -> Serializer:
        serializer = self.get_serializer(data=data)  # type: ignore
        serializer.is_valid(raise_exception=raise_exception)
        return serializer
