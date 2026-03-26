"""
SQLite in-memory DB for tests (no PostgreSQL required).
Usage: python manage.py test --settings=config.settings_test
"""

from .settings import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
