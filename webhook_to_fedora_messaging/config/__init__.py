# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


import os
from logging import getLogger
from logging.config import dictConfig

from sqlalchemy_helpers import DatabaseManager

from webhook_to_fedora_messaging import database
from webhook_to_fedora_messaging.config import logger, standard


def get_config() -> dict:
    path = os.getenv("W2FM_CONFIG")
    confdict = {}
    with open(path) as file:
        exec(compile(file.read(), path, "exec"), confdict)  # noqa : S102
    standard.sync_database_url = confdict.get("sync_database_url", standard.sync_database_url)
    standard.async_database_url = confdict.get("async_database_url", standard.async_database_url)
    standard.service_host = confdict.get("service_host", standard.service_host)
    standard.service_port = confdict.get("service_port", standard.service_port)
    standard.reload_on_change = confdict.get("reload_on_change", standard.reload_on_change)
    standard.main_logger_conf = confdict.get("main_logger_conf", standard.main_logger_conf)
    standard.wsgi_logger_conf = confdict.get("wsgi_logger_conf", standard.wsgi_logger_conf)
    dictConfig(standard.main_logger_conf)
    logger.logger_object = getLogger(__name__)
    database.db = DatabaseManager(standard.sync_database_url, "webhook_to_fedora_messaging/migrations")
    logger.logger_object.info("Reading the configuration again")
