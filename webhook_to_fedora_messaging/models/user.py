# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Boolean, Column, Integer, UnicodeText

from webhook_to_fedora_messaging.database import Base
from webhook_to_fedora_messaging.models.util import CreatableMixin, UUIDCreatableMixin


class User(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=True, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
