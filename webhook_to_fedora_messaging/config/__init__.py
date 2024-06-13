# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from os import environ

import tomllib

from webhook_to_fedora_messaging.exceptions import ConfigError


def get_config():
    path = environ["W2FM_APPCONFIG"]
    try:
        with open(path, "rb") as file:
            return tomllib.load(file)["flaskapp"]
    except FileNotFoundError as expt:
        raise ConfigError(f"Configuration file '{path}' was not found")
    except KeyError as expt:
        raise ConfigError(f"Configuration key '{expt}' could not be read")
