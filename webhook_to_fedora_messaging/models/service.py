# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Column, Integer, UnicodeText, Boolean, ForeignKey
from webhook_to_fedora_messaging.models.util import UUIDCreatableMixin, CreatableMixin

from webhook_to_fedora_messaging.database import Base

from uuid import uuid4


class Service(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=False, nullable=False)
    token = Column(UnicodeText, unique=False, nullable=False, default=uuid4().hex)
    name = Column(UnicodeText, nullable=False)
    type = Column(UnicodeText, nullable=False)
    desc = Column(UnicodeText, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
