class ActionSerializersMixin:
    """Mixin for ViewSets that allows to have a dict with a serializer for
    each action.
    """

    action_serializers = {}

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super().get_serializer_class()
