import os
import logging
from logging import Formatter, Logger
from logging.handlers import RotatingFileHandler
from datetime import datetime

INFO_LOG_DIRECTORY = os.environ.get('INFO_LOG_DIRECTORY')
ERROR_LOG_DIRECTORY = os.environ.get('ERROR_LOG_DIRECTORY')

INFO_MAX_GIGA_BYTES = int(os.environ.get('INFO_MAX_GIGA_BYTES')) * 1024 * 1024
INFO_BACKUP_COUNT = os.environ.get('INFO_BACKUP_COUNT')

ERROR_MAX_GIGA_BYTES = int(os.environ.get('ERROR_MAX_GIGA_BYTES')) * 1024 * 1024
ERROR_BACKUP_COUNT = os.environ.get('ERROR_BACKUP_COUNT')

FORMATTER = Formatter('%(process)d - %(levelname)s - %(asctime)s - %(message)s') 

handler = RotatingFileHandler(
    f"{INFO_LOG_DIRECTORY}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    , maxBytes=INFO_MAX_GIGA_BYTES
    , backupCount=INFO_BACKUP_COUNT)
handler.setFormatter(FORMATTER) 

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    f"{ERROR_LOG_DIRECTORY}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    , maxBytes=ERROR_MAX_GIGA_BYTES
    , backupCount=ERROR_BACKUP_COUNT)
handler.setFormatter(FORMATTER)

error_logger = logging.getLogger("error")
error_logger.addHandler(handler)
error_logger.setLevel(logging.ERROR)

def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    error_logger.error(msg, *args, **kwargs)
