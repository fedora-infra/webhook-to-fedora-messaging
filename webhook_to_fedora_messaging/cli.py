import logging
import os
from asyncio import run

import click

from webhook_to_fedora_messaging import __version__
from webhook_to_fedora_messaging.config import setup_config, setup_database_manager
from webhook_to_fedora_messaging.database import setup_database
from webhook_to_fedora_messaging.main import start_service


logger = logging.getLogger(__name__)


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
        setup_config()
    except FileNotFoundError:
        logger.error("Configuration file was not found")
        click.Abort()
    setup_database_manager()


@main.command(name="setup", help="Setup the database schema in the specified environment")
def setup():
    run(setup_database())


@main.command(name="start", help="Setup the application service")
def start():
    start_service()
