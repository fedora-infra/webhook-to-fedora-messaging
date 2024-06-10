# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cache
from pathlib import Path

from pydantic import BaseModel, ConfigDict, DirectoryPath
from pydantic_settings import BaseSettings
from webhook_to_fedora_messaging import defaults

from os.path import exists


projconf = None
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
    return Config(_env_file=config_file)


def set_config(path: str) -> None:
    if exists(path):
        defaults.config_file = path
        defaults.config = Config(_env_file=defaults.config_file)
        print(defaults.config, defaults.config_file)


def setconfig_file(path: str) -> None:
    global config_file
    config_file = path
    get_config.cache_clear()
