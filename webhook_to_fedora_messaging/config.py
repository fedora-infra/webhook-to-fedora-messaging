# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from functools import cache
from pathlib import Path
from secrets import token_urlsafe
from typing import Any

from pydantic import BaseModel, DirectoryPath, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_CONFIG_FILE = _config_file = os.getenv(
    "W2FM_CONFIG", "/etc/webhook-to-fedora-messaging/webhook-to-fedora-messaging.cfg"
)
TOP_DIR = Path(__file__).parent


class SQLAlchemyModel(BaseModel):
    model_config = SettingsConfigDict(extra="allow")

    url: str = f"sqlite:///{TOP_DIR.parent.joinpath('webhook-to-fedora-messaging.db').absolute()}"
    echo: bool = False


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = TOP_DIR.joinpath("migrations").absolute()


class DBModel(BaseModel):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


class OIDCModel(BaseModel):
    provider_url: str = "https://id.fedoraproject.org/openidc"
    client_id: str = "w2fm"
    scopes: str = " ".join(
        [
            "openid",
            "email",
            "profile",
            "https://id.fedoraproject.org/scope/groups",
            "https://id.fedoraproject.org/scope/agreements",
        ]
    )


class CacheModel(BaseModel):
    url: str = "mem://"
    setup_args: dict[str, Any] | None = None


def url_no_trailing_slash(url: str) -> str:
    return url.rstrip("/")


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    database: DBModel = DBModel()
    fasjson_url: str = "https://fasjson.fedoraproject.org"
    datagrepper_url: str = "https://apps.fedoraproject.org/datagrepper"
    logging_config: Path = Path("/etc/webhook-to-fedora-messaging/logging.yaml")
    oidc: OIDCModel = OIDCModel()
    cache: CacheModel = CacheModel()
    # It's fine if it changes on each startup: it's only used to temporarily store auth sessions
    session_secret: str = token_urlsafe(42)

    _normalize_fasjson_url = field_validator("fasjson_url")(url_no_trailing_slash)
    _normalize_datagrepper_url = field_validator("datagrepper_url")(url_no_trailing_slash)


@cache
def get_config() -> Config:
    return Config(_env_file=_config_file)  # pyright: ignore[reportCallIssue]


def set_config_file(path: str) -> None:
    global _config_file
    _config_file = path
    get_config.cache_clear()
