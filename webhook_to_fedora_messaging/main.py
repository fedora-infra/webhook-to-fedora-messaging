# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import click

from webhook_to_fedora_messaging import __version__
from webhook_to_fedora_messaging.config import set_config


@click.group(name="webhook-to-fedora-messaging")
@click.option(
    "-c",
    "--config",
    "config",
    type=click.Path(exists=True),
    default=None,
    required=True,
    help="Configure the service utility"
)
@click.version_option(
    version=__version__,
    prog_name="Webhook To Fedora Messaging",
)
def main(config: str) -> None:
    """
    Webhook To Fedora Messaging
    """
    set_config(config)


@main.command(
    name="service",
    help="Start the service utility",
    context_settings={"show_default": True},
)
@click.option(
    "-p",
    "--port",
    "port",
    type=click.IntRange(min=64, max=65535),
    default=8080,
    required=False,
    help="Set the port value for service utility endpoints"
)
@click.option(
    "-r",
    "--repair",
    "repair",
    type=bool,
    default=False,
    required=False,
    help="Show the nerdy statistics for debugging purposes"
)
def service(port: int = 8080, repair: bool = False) -> None:
    pass


@main.command(
    name="migrate",
    help="Setup the database models",
    context_settings={"show_default": True},
)
def migrate() -> None:
    pass
