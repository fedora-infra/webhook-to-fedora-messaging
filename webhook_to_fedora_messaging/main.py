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
from webhook_to_fedora_messaging.exceptions import ConfigError
import logging


def create_app():
    # Instantiate a barebones Flask application
    main = Flask(
	    "webhook_to_fedora_messaging"
    )
    # First attempt loading the defaults from the Defaults object
    main.config.from_object(
        "webhook_to_fedora_messaging.config.defaults.Defaults"
    )
    dictConfig(LOGGER_CONFIG)

    # Then load the variables up from the custom configuration file
    try:
        confdata = get_config()
    except ConfigError as expt:
        logging.error(f"Exiting - Reason - {str(expt)}")
        raise

    main.config.from_mapping(confdata)
    db.init_app(main)
    dictConfig(confdata["logsconf"])
    main.register_blueprint(user_endpoint)
    
    return main
