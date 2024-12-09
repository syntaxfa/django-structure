from functools import lru_cache

from django.conf import settings
from pkg.logger.base import Log
from pkg.logger.standard.logger import StandardLogger

logger_name = getattr(settings, "LOGGER_NAME", "standard")


@lru_cache
def _get_standard_logger_once() -> StandardLogger:
    return StandardLogger()


def get_logger() -> Log:
    match logger_name:
        case _:
            return _get_standard_logger_once()
