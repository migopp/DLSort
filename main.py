# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# import dependencies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
import shutil
import logging
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# set up user data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


user = "migopp"
source_dir = f"/Users/{user}/Downloads"
audio_dir = f"/Users/{user}/Documents/Audio"
video_dir = f"/Users/{user}/Documents/Video"
image_dir = f"/Users/{user}/Documents/Images"
doc_dir = f"/Users/{user}/Documents/Docs"

os.chdir(source_dir)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# establish attributes for sorting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


classes = [
    "314H", "311H", "340L", "303"
]

audio = [
    ".pcm", ".wav", ".aiff", ".mp3", ".aac",
    ".ogg", ".wma", ".flac", ".alac", ".wma"
]

video = [
    ".mp4", ".mov", ".wmv", ".avi", ".avchd",
    ".flv", ".f4v", ".swf", ".mkv", ".webm"
]

image = [
    ".jpeg", ".jpg", ".gif", ".psd", ".webp",
    ".raw", ".tiff", ".jfif", ".pjpeg", ".pfp",
    ".png", ".svg", ".apng", ".avif", ".eps"
]

doc = [
    ".pdf", ".docx", ".txt", ".oform", ".docxf",
    ".xlsx", ".pptx", ".odt", ".csv"
]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# sorting methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def is_class(file):
    for name in classes:
        if name in os.path.splitext(file)[0]:
            return True
    return False


def is_audio(file):
    return os.path.splitext(file)[1].lower() in audio


def is_video(file):
    return os.path.splitext(file)[1].lower() in video


def is_image(file):
    return os.path.splitext(file)[1].lower() in image


def is_doc(file):
    return os.path.splitext(file)[1].lower() in doc


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# establish behavior upon a change in the source directory
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class AutomatedMovingHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for entry in os.listdir():
            if (is_class(entry)):
                name = os.path.splitext(entry)[0]
                splitted = name.split("_")
                if (splitted[0].upper() == "CS" or splitted[0].upper() == "M"):
                    shutil.move(
                        entry, f"/Users/{user}/Documents/School/{splitted[0].upper()}/{splitted[1]}")
                    logging.info(
                        f"Moved school file {entry} to /Users/{user}/Documents/School/{splitted[0].upper()}/{splitted[1]}")
                else:
                    shutil.move(
                        entry, f"/Users/{user}/Documents/School/Other/{splitted[1]}")
                    logging.info(
                        f"Moved school file {entry} to /Users/{user}/Documents/School/Other/{splitted[1]}")
            elif (is_audio(entry)):
                shutil.move(entry, audio_dir)
                logging.info(f"Moved audio file {entry} to {audio_dir}")
            elif (is_video(entry)):
                shutil.move(entry, video_dir)
                logging.info(f"Moved video file {entry} to {video_dir}")
            elif (is_image(entry)):
                shutil.move(entry, image_dir)
                logging.info(f"Moved image file {entry} to {image_dir}")
            elif (is_doc(entry)):
                shutil.move(entry, doc_dir)
                logging.info(f"Moved document file {entry} to {doc_dir}")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# watchdog setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = AutomatedMovingHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
