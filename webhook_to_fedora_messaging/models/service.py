# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from uuid import uuid4

from sqlalchemy import Boolean, Column, Integer, UnicodeText, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base
from .owners import owners_table
from .util import CreatableMixin, UUIDCreatableMixin


class Service(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "services"
    __table_args__ = (UniqueConstraint("type", "name"),)

    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(UnicodeText, unique=False, nullable=False, default=uuid4().hex)
    name = Column(UnicodeText, nullable=False)
    type = Column(UnicodeText, nullable=False)
    desc = Column(UnicodeText, nullable=True)
    disabled = Column(Boolean, nullable=False, default=False)
    sent = Column(Integer, nullable=False, default=0)
    users = relationship("User", secondary=owners_table, back_populates="services")
