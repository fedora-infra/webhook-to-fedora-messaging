# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from uuid import uuid4

from sqlalchemy import Boolean, Column, ForeignKey, Integer, UnicodeText, UniqueConstraint

from webhook_to_fedora_messaging.database import Base
from webhook_to_fedora_messaging.models.util import CreatableMixin, UUIDCreatableMixin


class Service(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "services"
    __table_args__ = (UniqueConstraint("type", "name"),)

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=False, nullable=False
    )
    token = Column(UnicodeText, unique=False, nullable=False, default=uuid4().hex)
    name = Column(UnicodeText, nullable=False)
    type = Column(UnicodeText, nullable=False)
    desc = Column(UnicodeText, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
