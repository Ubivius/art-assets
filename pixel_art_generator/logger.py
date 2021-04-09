import logging
import sys

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.propagate = False



