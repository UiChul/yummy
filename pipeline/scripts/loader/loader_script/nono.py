import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run

    def on_modified(self, event):
        if event.src_path == "/home/rapa/yummy/pipeline/json/webhooks_report.json":
            print (f"{event.src_path} has been modified")
            subprocess.run(["python3.9", self.script_to_run])

if __name__ =="__main__":
    path = "/home/rapa/yummy/pipeline/json"
    event_handler = ChangeHandler(script_to_run="get_datas_for_user.py")
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

