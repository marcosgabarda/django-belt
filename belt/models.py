import io
import warnings
from typing import Dict, List, Optional, Tuple

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from belt.files import UploadToDir


class LogicDeleteMixin(models.Model):
    """Mixin to handle basic functionality of a logic delete"""

    deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def pre_logic_delete(self):
        pass

    def post_logic_delete(self):
        pass

    def pre_undo_logic_delete(self):
        pass

    def post_undo_logic_delete(self):
        pass

    def logic_delete(self):
        """Performs a logic delete for the object."""
        self.pre_logic_delete()
        self.deleted = True
        self.date_deleted = timezone.now()
        self.save()
        self.post_logic_delete()

    def undo_logic_delete(self):
        """Undoes the logic delete."""
        self.pre_undo_logic_delete()
        self.deleted = False
        self.date_deleted = None
        self.save()
        self.post_undo_logic_delete()


def transition_handler_decorator(func):
    """Decorator for transitions methods. Allows to activate a flag if the
    transition is running, and also saves the original status value.
    """
    if not func:
        return func

    def _transition_wrapper(self=None, *args, **kwargs):
        self._original_status = getattr(self, self.STATUS_FIELD)
        self._handling_transition = True
        result = func(*args, **kwargs)
        self._handling_transition = False
        return result

    return _transition_wrapper


class StatusMixin(models.Model):
    """Mixin to handle status changes"""

    STATUS_FIELD: str = "status"
    ALLOWED_TRANSITIONS: List[Tuple[str, str]] = []
    FORBIDDEN_TRANSITIONS: List[Tuple[str, str]] = []
    TRANSITION_HANDLERS: Dict[Tuple[str, str], str] = {}

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Init _handling_transition value to False."""
        self._handling_transition: bool = False
        super().__init__(*args, **kwargs)
        self._original_status = getattr(self, self.STATUS_FIELD)

    def refresh_from_db(self, using=None, fields=None):
        super().refresh_from_db(using=using, fields=fields)
        if hasattr(self, "_transition"):
            delattr(self, "_transition")

    def get_status_transition(self) -> Optional[Tuple[str, str]]:
        """Get status transition."""
        if self.pk:
            if hasattr(self, "_transition"):
                return self._transition
            previous = self._meta.model.objects.get(pk=self.pk)
            if previous.status != getattr(self, self.STATUS_FIELD):
                self._transition: Tuple[str, str] = (
                    previous.status,
                    getattr(self, self.STATUS_FIELD),
                )
                return self._transition
        return None

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

    def pre_status_handler(self, transition: Tuple[str, str]):
        """Method used to execute code before the status handler is called."""
        pass

    def post_status_handler(self, transition: Tuple[str, str]):
        """Method used to execute code after the status handler is called."""
        pass

    def get_transition_handler(self):
        """Get the transition handler between status."""
        transition = self.get_status_transition()
        if transition:
            handler_name = self.TRANSITION_HANDLERS.get(transition, "")
            transition_handler = (
                getattr(self, handler_name) if hasattr(self, handler_name) else None
            )
            return transition_handler_decorator(transition_handler)

    def clean(self):
        """Validates transition in clean."""
        self.validate_transition()

    def save(self, *args, **kwargs):
        # Checks if the is a transition during a handling
        if self._handling_transition and self._original_status != getattr(
            self, self.STATUS_FIELD
        ):
            setattr(self, self.STATUS_FIELD, self._original_status)
            warnings.warn(
                Warning(
                    "Status changes during the execution of transitions handlers are not allowed"
                )
            )
        # Gets the handler before the save
        transition = self.get_status_transition()
        transition_handler = self.get_transition_handler()
        super().save(*args, **kwargs)
        # Executes the handler after the save
        if transition_handler and not self._handling_transition:
            self.pre_status_handler(transition)
            transition_handler(self)
            self.post_status_handler(transition)


class ExporterModel(models.Model):

    IDLE, RUNNING, FINISHED, ERROR = 0, 1, 2, 3
    STATUSES = (
        (IDLE, _("Idle")),
        (RUNNING, _("Running")),
        (FINISHED, _("Finished")),
        (ERROR, _("Error")),
    )

    data = models.FileField(
        _("data"),
        upload_to=UploadToDir("export", random_name=True),
        null=True,
        blank=True,
    )

    status = models.SmallIntegerField(
        _("status"), choices=STATUSES, default=IDLE, blank=True
    )
    items = models.PositiveIntegerField(_("items"), null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Exporter #{self.pk}"

    def get_queryset(self):
        """Gets the QuerySet to export."""
        raise NotImplementedError()

    def exporter(self):
        """Gets the import helper function that does the export."""
        raise NotImplementedError()

    def exporter_task(self):
        """Gets the async task that does the exporter."""
        raise NotImplementedError()

    def export_data(self, async_process=False):
        """Executes the import process."""
        if self.status != self.IDLE:
            return  # Only import if is idle
        if async_process:
            task = self.exporter_task()
            task.delay(self.pk)
        else:
            self.items = 0
            self.status = self.RUNNING
            self.save()
            # Export data and save it in the file field
            exporter = self.exporter()
            output = io.StringIO()
            items = exporter(self.get_queryset(), output)
            output.seek(0)
            content = output.getvalue()
            self.data.save("export.csv", content=ContentFile(content.encode("utf-8")))
            self.items = items
            self.status = self.FINISHED
            self.save()


class ImporterModel(models.Model):
    """Abstract model to implement an asynchronous import process."""

    IDLE, RUNNING, FINISHED, ERROR = 0, 1, 2, 3
    STATUSES = (
        (IDLE, _("Idle")),
        (RUNNING, _("Running")),
        (FINISHED, _("Finished")),
        (ERROR, _("Error")),
    )

    data = models.FileField(
        _("data"), upload_to=UploadToDir("imports", random_name=False)
    )

    status = models.SmallIntegerField(
        _("status"), choices=STATUSES, default=IDLE, blank=True
    )
    items = models.PositiveIntegerField(_("items"), null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Importer #{self.pk}"

    def source(self):
        """Creates the source for the importer using the data file."""
        file_content = self.data.read()
        source = io.BytesIO()
        source.write(file_content)
        source.seek(0)
        return source

    def importer(self):
        """Gets the import helper function that does the import."""
        raise NotImplementedError()

    def importer_task(self):
        """Gets the async task that does the import."""
        raise NotImplementedError()

    def import_data(self, async_process=False):
        """Executes the import process."""
        if self.status != self.IDLE:
            return  # Only import if is idle
        if async_process:
            task = self.importer_task()
            task.delay(self.pk)
        else:
            self.items = 0
            self.status = self.RUNNING
            self.save()
            # Import line by line to don't load all the file in memory
            self.data.seek(0)
            importer = self.importer()
            try:
                items = importer(source=self.source())
                self.items = items.count()
                self.status = self.FINISHED
                self.save()
            except Exception as exception:
                self.status = self.ERROR
                self.save()
                raise exception
