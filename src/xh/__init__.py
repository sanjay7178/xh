"""Xhell."""

import sys

from importlib import metadata as importlib_metadata
from types import ModuleType
from typing import Any

# On non-Windows platforms, try to use sh; otherwise, use xh.core.
if sys.platform != 'win32':
    try:
        import sh

        from sh import Command

        _xh_backend = sh
    except ImportError:
        from xh.core import Command, CommandResult
        from xh.core import xh as _xh_backend
else:
    from xh.core import Command, CommandResult
    from xh.core import xh as _xh_backend


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return '0.2.0'  # semantic-release


version = get_version()

__version__ = version
__author__ = 'Ivan Ogasawara'
__email__ = 'ivan.ogasawara@gmail.com'

xh = _xh_backend


class XHModule(ModuleType):
    """
    XHModule acts like an xh backend instance.

    This allows both direct imports from the module and attribute access on the
    module.
    """

    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the backend."""
        return getattr(_xh_backend, name)


# Replace this module with our custom module
sys.modules[__name__] = XHModule(__name__)

# Export the CommandResult for Windows or when sh is not available
if sys.platform == 'win32' or 'sh' not in sys.modules:
    __all__ = ['Command', 'CommandResult', 'xh']
else:
    __all__ = ['Command', 'xh']
