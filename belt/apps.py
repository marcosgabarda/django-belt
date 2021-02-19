from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BeltConfig(AppConfig):
    """Django Belt AppConfig."""

    name = "belt"
    verbose_name = _("Belt")
