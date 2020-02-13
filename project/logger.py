import sys

from logging import Formatter, getLogger, INFO, DEBUG, StreamHandler


DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'


def configure_logging():
    logger = getLogger()

    handler = StreamHandler(sys.stdout)
    formatter = Formatter(LOGGING_FORMAT, DATE_TIME_FORMAT)

    handler.setLevel(INFO)
    handler.setFormatter(formatter)

    logger.setLevel(DEBUG)
    logger.addHandler(handler)
