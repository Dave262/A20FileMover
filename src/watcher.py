import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.start_script()

    def start_script(self):
        self.process = subprocess.Popen(["python", self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Change detected: {event.src_path}")
            self.process.terminate()  # Stop the previous process
            self.start_script()  # Start a new one


if __name__ == "__main__":
    path = "."  # Directory to watch
    script_to_run = "src/app.py"  # Your main script here
    event_handler = ReloadHandler(script_to_run)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
