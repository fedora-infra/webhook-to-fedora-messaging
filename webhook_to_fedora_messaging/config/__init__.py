# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


import logging
import os
from logging.config import dictConfig
from pathlib import Path

from sqlalchemy_helpers.fastapi import AsyncDatabaseManager

from webhook_to_fedora_messaging import database
from webhook_to_fedora_messaging.config import standard


logger = logging.getLogger(__name__)


def setup_config():
    path = os.getenv("W2FM_CONFIG")
    confdict = {}

    with open(path) as file:
        exec(compile(file.read(), path, "exec"), confdict)  # noqa : S102

    confkeys = (
        "database_url",
        "service_host",
        "service_port",
        "reload_on_change",
        "main_logger_conf",
        "wsgi_logger_conf",
        "fasjson_url",
    )
    for conf in confkeys:
        if conf not in confdict:
            continue
        setattr(standard, conf, confdict[conf])
    dictConfig(standard.main_logger_conf)
    logger.info("Reading the configuration.")


def setup_database_manager() -> None:
    database.db = AsyncDatabaseManager(
        standard.database_url,
        Path(__file__).parent.parent.joinpath("migrations").as_posix(),
        # engine_args={"echo": True},
    )
