from pathlib import Path
import json
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



import os

def is_file_stable(path: Path, wait_time=20) -> bool:
    """
    Check if the file size stays the same for `wait_time` seconds.
    Returns True if stable, False if still being written.
    """
    if not path.exists():
        return False

    initial_size = path.stat().st_size
    time.sleep(wait_time)
    return path.exists() and path.stat().st_size == initial_size


rules = json.load(open("rules.json"))["rules"]
home = Path.home()
download_dir = home / "Downloads"

# base names we manage
managed = {"Documents", "Images", "Executables", "Textfiles", "Unknown"}

# extensions of temporary files
TEMP_EXTS = {".crdownload", ".part", ".tmp"}

def valid_name(path, name):
    folder = path / name
    if folder.exists() and folder.is_dir():
        return folder
    elif folder.exists() and not folder.is_dir():
        return valid_name(path, name + "1")
    else:
        return folder


def mark_managed(folder: Path):
    """Ensure folder exists, create a hidden marker, and register the folder name."""
    folder.mkdir(parents=True, exist_ok=True)
    marker = folder / ".fileorganizer"
    if not marker.exists():
        marker.write_text("managed by file-organizer")
    managed.add(folder.name)


def is_managed_folder(folder: Path) -> bool:
    """Return True if folder is one of our managed folders (by name or marker)."""
    return folder.name in managed or (folder.is_dir() and (folder / ".fileorganizer").exists())


def move_item(src: Path, des: Path):
    """Move src into des, skip managed folders."""
    if src.is_dir() and is_managed_folder(src):
        return
    shutil.move(str(src), str(des / src.name))

def organize_downloads():
    """Scan and organize all files in Downloads."""
    for item in download_dir.iterdir():
        if item.is_dir() and is_managed_folder(item):
            continue
        if not item.exists():
            continue
        if not is_file_stable(item):
            continue  # skip files still being written

        suffix1 = item.suffix.lower()
        if suffix1 in TEMP_EXTS:
            continue
        elif suffix1 in rules[0]:
            dst = valid_name(download_dir, "Documents")
        elif suffix1 in rules[1]:
            dst = valid_name(download_dir, "Images")
        elif suffix1 in rules[2]:
            dst = valid_name(download_dir, "Executables")
        elif suffix1 in rules[3]:
            dst = valid_name(download_dir, "Textfiles")
        else:
            dst = valid_name(download_dir, "Unknown")

        mark_managed(dst)
        move_item(item, dst)



def wait_until_stable(path: Path, timeout: int = 30, interval: float = 20.0) -> bool:
    """
    Wait until file is stable (size stops changing).
    Returns True if stable within timeout, False otherwise.
    """
    if not path.exists():
        return False

    last_size = -1
    elapsed = 0
    while elapsed < timeout:
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False  # file vanished
        if size == last_size:
            return True
        last_size = size
        time.sleep(interval)
        elapsed += interval
    return False




class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            organize_downloads()

    def on_moved(self, event):
        if not event.is_directory:
            file_path = Path(event.dest_path)
            print(f"File renamed/moved: {file_path}")
            if wait_until_stable(file_path):  # 👈 wait until fully downloaded
                organize_downloads()


if __name__ == "__main__":
    # Initial run
    organize_downloads()

    # Start watchdog observer
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, str(download_dir), recursive=False)
    observer.start()
    print(f"Watching {download_dir}...")

    try:
        while True:
            time.sleep(100)  # every 10 seconds, check again
            organize_downloads()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
