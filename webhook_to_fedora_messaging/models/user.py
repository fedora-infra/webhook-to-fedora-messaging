# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Column, Integer, UnicodeText, Boolean
from webhook_to_fedora_messaging.models.util import UUIDCreatableMixin, CreatableMixin

from webhook_to_fedora_messaging.database import Base


class User(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(UnicodeText, unique=True, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
