import sys
import time
import logging
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_created(self, event):
        newEmail = event.src_path[event.src_path.index("/")+1:len(event.src_path)]
        if not event.is_directory:
            print "file created"
            self.observer.stop()
            
print "Started"
path = "new_signups/"
observer = Observer()
event_handler = MyEventHandler(observer)
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
