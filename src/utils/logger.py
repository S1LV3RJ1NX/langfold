import logging
import sys

from src.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)
formatter = logging.Formatter(
    "[PID:%(process)d/%(processName)s][%(thread)d/%(threadName)s] %(levelname)s:    %(asctime)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"
)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
