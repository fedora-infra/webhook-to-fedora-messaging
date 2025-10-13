# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .owners import owners_table
from .util import CreatableMixin, UUIDCreatableMixin


if TYPE_CHECKING:
    from .user import User


class Service(Base, UUIDCreatableMixin, CreatableMixin):
    __tablename__ = "services"
    __table_args__ = (UniqueConstraint("type", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=False, default=uuid4().hex)
    name: Mapped[str]
    type: Mapped[str]
    desc: Mapped[str | None]
    disabled: Mapped[bool] = mapped_column(default=False)
    sent: Mapped[int] = mapped_column(default=0)
    users: Mapped[list["User"]] = relationship(secondary=owners_table, back_populates="services")
