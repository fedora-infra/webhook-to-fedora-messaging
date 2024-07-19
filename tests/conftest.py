# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest  # noqa: F401

from webhook_to_fedora_messaging.database import db  # noqa: F401
from sqlalchemy_helpers import get_or_create
from webhook_to_fedora_messaging.main import create_app
from os import environ
from os.path import abspath, basename
from webhook_to_fedora_messaging.models.user import User
from webhook_to_fedora_messaging.models.service import Service


@pytest.fixture(scope="session")
def client():
    root = abspath(__name__)
    environ["W2FM_APPCONFIG"] = root.replace(basename(root), "tests/data/test.toml")
    with open("/tmp/w2fm-test.db", "wb") as dest:
        with open(root.replace(basename(root), "tests/data/w2fm-test.db"), "rb") as srce:
            dest.write(srce.read())
    return create_app().test_client()


@pytest.fixture(autouse=False, scope="function")
def create_user(client):
    with client.application.app_context():
        # Setup code to create the object in the database
        user, is_created = get_or_create(db.session, User, username="mehmet") # Adjust fields as necessary
        db.session.commit()

    yield

    with client.application.app_context():
        # Teardown code to remove the object from the database
        db.session.query(User).filter_by(username="mehmet").delete()
        db.session.commit()
    
    
@pytest.fixture(autouse=False, scope="function")
def create_service(client):
    with client.application.app_context():
        # Setup code to create the object in the database
        user, created = get_or_create(db.session, User, username="mehmet") # Adjust fields as necessary
        get_or_create(db.session, Service, name="Github Demo", type="Github", desc="description", user_id=user.id)

        db.session.commit()

    yield

    with client.application.app_context():
        # Teardown code to remove the object from the database
        db.session.query(User).filter_by(username="mehmet").delete()
        db.session.query(Service).filter_by(name="Github Demo").delete()
        db.session.commit()

