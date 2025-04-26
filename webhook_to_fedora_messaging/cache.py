import logging

from cashews import cache

from .config import get_config


log = logging.getLogger(__name__)


def configure_cache() -> None:
    config = get_config()
    args = config.cache.setup_args or {}
    cache.setup(config.cache.url, **args)
