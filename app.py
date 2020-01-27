import pyinotify
import os
from pathlib import Path
import logging
from logging import Formatter, Logger
from logging.handlers import RotatingFileHandler
from datetime import datetime

SOURCE = os.environ.get('APP_SOURCE')
DESTINATION = os.environ.get('APP_DESTINATION')

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

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        logger.info("%s has been added", event.name)        
        dest_path = DESTINATION + event.pathname.replace(SOURCE, '')
        dest_dir = dest_path.replace(event.name, '')

        try:
            if os.path.isdir(dest_dir) == False:
                os.makedirs(dest_dir)
                logger.info("%s directory has been made", dest_dir)

            Path(dest_path).touch()
            logger.info("%s has been touched", dest_path)
        except Exception as e:
            error_logger.error(e, exc_info=True)


wm = pyinotify.WatchManager()
wm.add_watch(SOURCE, pyinotify.ALL_EVENTS, rec=True)

# event handler
eh = MyEventHandler()

# notifier
notifier = pyinotify.Notifier(wm, eh)
notifier.loop()
