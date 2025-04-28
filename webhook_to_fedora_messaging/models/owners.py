from sqlalchemy import Column, ForeignKey, Table

from ..database import Base


# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
owners_table = Table(
    "owners",
    Base.metadata,
    Column("service_id", ForeignKey("services.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)
