# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from typing import Any

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

from webhook_to_fedora_messaging import models  # noqa: F401
from webhook_to_fedora_messaging.config import get_config
from webhook_to_fedora_messaging.database import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# logging.config.fileConfig(alembic_config.config_file_name)
logger = logging.getLogger("alembic.env")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = alembic_config.get_main_option("my_important_option")
# ... etc.

url = get_config().database.sqlalchemy.url
alembic_config.set_main_option("sqlalchemy.url", url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context: Any, revision: Any, directives: Any) -> None:
        if getattr(alembic_config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_sync_migrations() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


def run_migrations_online() -> None:
    connectable = alembic_config.attributes.get("connection", None)

    if connectable is None:
        run_sync_migrations()
    else:
        do_run_migrations(connectable)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
