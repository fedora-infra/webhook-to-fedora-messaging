# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cache
from pathlib import Path

from pydantic import BaseModel, ConfigDict, DirectoryPath
from pydantic_settings import BaseSettings


DEFAULT_CONFIG_FILE = _config_file = "/etc/webhook-to-fedora-messaging/webhook-to-fedora-messaging.cfg"
TOP_DIR = Path(__file__).parent


class SQLAlchemyModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str = f"sqlite:///{TOP_DIR.parent.joinpath('webhook-to-fedora-messaging.db').absolute()}"
    echo: bool = False
    isolation_level: str = "SERIALIZABLE"


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = TOP_DIR.joinpath("migrations").absolute()


class DBModel(BaseModel):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


class Config(BaseSettings):
    database: DBModel = DBModel()


@cache
def get_config() -> Config:
    return Config(_env_file=_config_file)


def set_config_file(path: str) -> None:
    global _config_file
    _config_file = path
    get_config.cache_clear()
