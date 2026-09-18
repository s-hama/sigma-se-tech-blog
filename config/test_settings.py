"""Run tests with an isolated SQLite database and no production log files."""

from .settings import *  # noqa: F403


SECRET_KEY = "sigma-se-local-tests-only"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1", "sigma-se.com", "www.sigma-se.com"]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
LOGGING = {"version": 1, "disable_existing_loggers": False}
