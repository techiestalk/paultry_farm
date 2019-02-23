from paultry_farm.constants import APP_LOG_PATH, LOG_FORMATTER, LOG_TIME_FMT
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(LOG_FORMATTER, LOG_TIME_FMT)

file_handler = logging.FileHandler(APP_LOG_PATH)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
