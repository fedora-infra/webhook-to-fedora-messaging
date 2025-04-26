import logging
import sys
import traceback

import backoff
from fastapi.concurrency import run_in_threadpool
from fedora_messaging import api
from fedora_messaging import exceptions as fm_exceptions


log = logging.getLogger(__name__)


def backoff_hdlr(details) -> None:
    log.warning("Publishing message failed. Retrying. %s", traceback.format_tb(sys.exc_info()[2]))


def giveup_hdlr(details) -> None:
    log.error("Publishing message failed. Giving up. %s", traceback.format_tb(sys.exc_info()[2]))


@backoff.on_exception(
    backoff.expo,
    (fm_exceptions.ConnectionException, fm_exceptions.PublishException),
    max_tries=3,
    on_backoff=backoff_hdlr,
    on_giveup=giveup_hdlr,
)
async def publish(message: api.Message) -> None:
    await run_in_threadpool(api.publish, message)
