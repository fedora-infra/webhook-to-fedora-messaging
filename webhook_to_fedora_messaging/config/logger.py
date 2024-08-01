import logging


logging.basicConfig(
    format="[W2FM] %(asctime)s [%(levelname)s] %(message)s",
    datefmt="[%Y-%m-%d %I:%M:%S %z]",
    level=logging.INFO,
)

logger_object = logging.getLogger(__name__)
