# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The values for any configuration variable that was not mentioned of in the
custom configuration file will be inherently taken from the default values
"""


from flask import Flask
from webhook_to_fedora_messaging.database import db
from .config import get_config
from .config.defaults import LOGGER_CONFIG
from logging.config import dictConfig
from .endpoints.user import user_endpoint
from .endpoints.message import message_endpoint
from .endpoints.service import service_endpoint
from webhook_to_fedora_messaging.exceptions import ConfigError
import logging


def create_app():
    # Instantiate a barebones Flask application
    app = Flask(
	    "webhook_to_fedora_messaging"
    )
    # First attempt loading the defaults from the Defaults object
    app.config.from_object(
        "webhook_to_fedora_messaging.config.defaults.Defaults"
    )
    dictConfig(LOGGER_CONFIG)

    app.register_blueprint(user_endpoint, url_prefix="/user")
    app.register_blueprint(service_endpoint, url_prefix="/service")
    app.register_blueprint(message_endpoint, url_prefix="/message")

    # Then load the variables up from the custom configuration file
    try:
        confdata = get_config()
    except ConfigError as expt:
        logging.error(f"Exiting - Reason - {str(expt)}")
        raise

    app.config.from_mapping(confdata)
    db.init_app(app)
    dictConfig(confdata["logsconf"])
    
    return app
