from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class StatusMixin(models.Model):
    """Mixin to handle status changes"""

    STATUS_FIELD = "status"
    ALLOWED_TRANSITIONS = []
    FORBIDDEN_TRANSITIONS = []
    TRANSITION_HANDLERS = {}

    class Meta:
        abstract = True

    def refresh_from_db(self, using=None, fields=None):
        super().refresh_from_db(using=using, fields=fields)
        if hasattr(self, "_transition"):
            delattr(self, "_transition")

    def get_status_transition(self):
        """Get status transition."""
        if self.pk:
            if hasattr(self, "_transition"):
                return self._transition
            previous = self._meta.model.objects.get(pk=self.pk)
            if previous.status != getattr(self, self.STATUS_FIELD):
                self._transition = previous.status, getattr(self, self.STATUS_FIELD)
                return self._transition

    def validate_transition(self):
        """Validates the transition."""
        transition = self.get_status_transition()
        # Check the transition is not a allowed transitions
        if (
            transition
            and self.ALLOWED_TRANSITIONS
            and transition not in self.ALLOWED_TRANSITIONS
        ):
            raise ValidationError(
                _(
                    f"A {self._meta.model_name} can't change from "
                    f"{transition[0]} to {transition[1]}"
                )
            )
        # Check the transition is not a forbidden transitions
        if (
            transition
            and self.FORBIDDEN_TRANSITIONS
            and transition in self.FORBIDDEN_TRANSITIONS
        ):
            raise ValidationError(
                _(
                    f"A {self._meta.model_name} can't change from "
                    f"{transition[0]} to {transition[1]}"
                )
            )

    def pre_status_handler(self, transition):
        """Method used to execute code before the status handler is called."""
        pass

    def post_status_handler(self, transition):
        """Method used to execute code after the status handler is called."""
        pass

    def get_transition_handler(self):
        """Get the transition handler between status."""
        transition = self.get_status_transition()
        if transition:
            handler_name = self.TRANSITION_HANDLERS.get(transition, "")
            return getattr(self, handler_name) if hasattr(self, handler_name) else None

    def clean(self):
        """Validates transition in clean."""
        self.validate_transition()

    def save(self, *args, **kwargs):
        # Gets the handler before the save
        transition = self.get_status_transition()
        transition_handler = self.get_transition_handler()
        super().save(*args, **kwargs)
        # Executes the handler after the save
        if transition_handler:
            self.pre_status_handler(transition)
            transition_handler()
            self.post_status_handler(transition)
