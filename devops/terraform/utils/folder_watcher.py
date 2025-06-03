import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.blob_uploader import upload_to_blob

WATCH_FOLDER = "data_simulator/landing"

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".json"):
            print(f"📦 New JSON file detected: {event.src_path}")
            try:
                domain = event.src_path.split(os.sep)[-2]  # get domain from folder path
                upload_to_blob(event.src_path, layer="bronze", domain=domain)
            except Exception as e:
                print(f"❌ Failed to detect domain or upload file: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(NewFileHandler(), path=WATCH_FOLDER, recursive=True)
    observer.start()
    print("👀 Watching folder for new JSON files... Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
