# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


class Defaults:
    DEBUG = False
    # The session information will be retained for 6 months
    PERMANENT_SESSION_LIFETIME = 604800
    SESSION_COOKIE_NAME = "user"


LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "level": "DEBUG",
            "formatter": "default",
        },
    },
    "formatters": {
        "default": {
            "format": "[W2FM] %(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "root": {
        "handlers": ["wsgi"],
        "level": "DEBUG",
    },
    "loggers": {
        "werkzeug": {
            "handlers": ["wsgi"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}
