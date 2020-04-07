from rest_framework.fields import Field, SerializerMethodField


class AnnotatedField(Field):
    """
    A read-only field that automatically returns an annotated field, taking
    into account a default value if the property is not found and if the user
    is present in the request
    """

    def __init__(self, default_value=None, requires_user=False, **kwargs):
        self.default_value = default_value
        self.requires_user = requires_user
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def get_value(self, instance):
        if self.requires_user and (
            "request" not in self.context
            or not self.context["request"].user.is_authenticated
        ):
            return self.default_value

        try:
            value = getattr(instance, self.field_name)
        except AttributeError:
            value = self.default_value

        return value

    def to_representation(self, value):
        return self.get_value(value)
