# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .owners import owners_table
from .util import CreatableMixin

if TYPE_CHECKING:
    from .service import Service


class User(Base, CreatableMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    services: Mapped[list["Service"]] = relationship(secondary=owners_table, back_populates="users")
