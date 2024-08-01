import os
import sys
from asyncio import run

import click

from webhook_to_fedora_messaging import __version__
from webhook_to_fedora_messaging.config import get_config, logger
from webhook_to_fedora_messaging.database import setup_database
from webhook_to_fedora_messaging.main import start_service


@click.group()
@click.option(
    "-c",
    "--conf",
    "conf",
    type=click.Path(exists=True),
    help="Read configuration from the specified module",
    default=None,
)
@click.version_option(version=__version__, prog_name="w2fm")
def main(conf=None):
    if conf:
        os.environ["W2FM_CONFIG"] = os.path.abspath(conf)
    try:
        get_config()
    except FileNotFoundError:
        logger.logger_object.error("Configuration file was not found")
        sys.exit(1)


@main.command(name="setup", help="Setup the database schema in the specified environment")
def setup():
    run(setup_database())


@main.command(name="start", help="Setup the application service")
def start():
    start_service()
