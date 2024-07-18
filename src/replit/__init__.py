# flake8: noqa

"""The Replit Python module."""

try:
    # This is inlined from https://github.com/replit/replit-py/blob/master/src/replit/__init__.py
    # See https://github.com/replit/replit-object-storage-python/issues/13 for context
    from typing import Any
    from . import database, web
    from .database import (
        Database,
        AsyncDatabase,
        make_database_proxy_blueprint,
        start_database_proxy,
    )
    from .info import ReplInfo

    info = ReplInfo()

    # Backwards compatibility.
    def clear() -> None:
        """Clear the terminal."""
        print("\033[H\033[2J", end="", flush=True)

    # Previous versions of this library would just have side-effects and always set
    # up a database unconditionally. That is very undesirable, so instead of doing
    # that, we are using this egregious hack to get the database / database URL
    # lazily.
    def __getattr__(name: str) -> Any:
        if name == "db":
            return database.db
        raise AttributeError(name)

except ImportError:
    pass
