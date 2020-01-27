import pyinotify
import os
from pathlib import Path

source = '/home/arash/sources/data'
dest = '/home/arash/sources/dest'

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        print("CLOSE_WRITE event:", event.pathname)        
        dest_path = dest + event.pathname.replace(source, '')
        dest_dir = dest_path.replace(event.name, '')

        try:
            if os.path.isdir(dest_dir) == False:
                os.makedirs(dest_dir)

            Path(dest_path).touch()
        except:
            print ("Creation of the directory %s failed" % dest_path)
        else:
            print ("Successfully created the directory %s" % dest_path)

# watch manager
wm = pyinotify.WatchManager()
wm.add_watch(source, pyinotify.IN_CLOSE_WRITE, rec=True)

# event handler
eh = MyEventHandler()

# notifier
notifier = pyinotify.Notifier(wm, eh)
notifier.loop()
