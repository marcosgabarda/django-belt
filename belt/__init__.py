"""Django app made to get together a set of utilities to use with Django projects."""
from pathlib import Path

from single_source import get_version

__version__ = get_version(__name__, Path(__file__).parent.parent) or "1.0.0"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)


default_app_config = "belt.apps.BeltConfig"
