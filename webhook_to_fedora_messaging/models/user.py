# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from . import service
from .owners import owners_table
from .util import CreatableMixin


class User(Base, CreatableMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    services: Mapped[list["service.Service"]] = relationship(
        secondary=owners_table, back_populates="users"
    )
