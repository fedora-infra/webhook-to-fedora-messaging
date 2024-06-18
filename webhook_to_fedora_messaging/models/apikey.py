# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Column, Integer, UnicodeText, Boolean, ForeignKey, DateTime
from webhook_to_fedora_messaging.models.util import UUIDCreatableMixin, CreatableMixin

from webhook_to_fedora_messaging.database import Base

from uuid import uuid4


class APIKey(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "apikeys"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=False, nullable=False)
    name = Column(UnicodeText, nullable=False)
    token = Column(UnicodeText, unique=True, nullable=False, default=uuid4().hex)
    expiry_date = Column(DateTime, nullable=True)
    disabled = Column(Boolean, nullable=False, default=False)
