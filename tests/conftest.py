# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest  # noqa: F401

from webhook_to_fedora_messaging.database import db  # noqa: F401

from webhook_to_fedora_messaging.main import create_app
from os import environ
from os.path import abspath, basename


@pytest.fixture(scope="session")
def client():
    root = abspath(__name__)
    environ["W2FM_APPCONFIG"] = root.replace(basename(root), "tests/data/test.toml")
    with open("/tmp/w2fm-test.db", "wb") as dest:
        with open(root.replace(basename(root), "tests/data/w2fm-test.db"), "rb") as srce:
            dest.write(srce.read())
    return create_app().test_client()
