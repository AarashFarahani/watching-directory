import os
import pyinotify
from pathlib import Path
import log_handler

class MyEventHandler(pyinotify.ProcessEvent):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def process_IN_CLOSE_WRITE(self, event):
        log_handler.info("%s has been added", event.name)        
        _touch(self.source, self.destination, event.pathname, event.name)


def _touch(source, destination, file_path, file_name):
    dest_path = destination + file_path.replace(source, '')
    dest_dir = dest_path.replace(file_name, '')

    try:
        if os.path.isdir(dest_dir) == False:
            os.makedirs(dest_dir)
            log_handler.info("%s directory has been made", dest_dir)

        Path(dest_path).touch()
        log_handler.info("%s has been touched", dest_path)
    except Exception as e:
        print(e)
        log_handler.error(e, exc_info=True)


def start_watching(source, destination):
    wm = pyinotify.WatchManager()
    wm.add_watch(source, pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = MyEventHandler(source, destination)

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

def touch_exist_files(source, destination):
    dict = {}
    for r, d, f in os.walk(source):
        for file in f:
            dict[os.path.join(r, file)] = file

    for file_path, file_name in dict.items():
        _touch(source, destination, file_path, file_name)
