# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Boolean, Column, Integer, UnicodeText
from sqlalchemy.orm import relationship

from ..database import Base
from .owners import owners_table
from .util import CreatableMixin


class User(Base, CreatableMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=True, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    services = relationship("Service", secondary=owners_table, back_populates="users")
