# DLSort 1.0
DLSort is a simple, Python-based file sorting script. I built it to automate the file organization on my machine running macOS—because why not have a computer do the work for you?

## How does DLSort work?
DLSort simply watches a given source directory for modifications, then uses an event handler to move newly-added files into predetermined directories based on their file extensions (or name contents, if you choose to adapt the "classes" feature).

## What's included here?
Inside this repository, you'll find dl_sort.py and requirements.txt. DLSort is a Python script that's intended to run in the shell, utilizing watchdog to detect changes in the source directory. It's indended to be an efficient script running in the background, launching upon start up. If you wish to use a virtual environment, utilize the requirements.txt file that I have included here. I will detail one way to set it up on your machine in the following section.

## How do I set it up on my machine?
I'll be catering these instructions toward macOS, because that is the operating system most familiar to me. It can also be used on other operating systems with some tweaking.

After downloading dl_sort.py, you'll need to edit some details within the script and create a new Unix Executable File for the shell to run DLSort.

### dl_sort.py
The section of code commented as "set up user data" will contain most of the necessary alterations within the Python script. I've pasted the section below:
```python
user = "migopp"
source_dir = f"/Users/{user}/Downloads"
audio_dir = f"/Users/{user}/Documents/Audio"
video_dir = f"/Users/{user}/Documents/Video"
image_dir = f"/Users/{user}/Documents/Images"
doc_dir = f"/Users/{user}/Documents/Docs"
```
**It should be noted that all of these directories must exist before you run the Python script. DLSort will not create them for you in its current iteration**

In place of the user variable, you will need to put the name of your user on your machine. Then, (depending on your needs), you may choose to change the source_dir variable (the source directory, and the place that watchdog will look for modifications).

For instance, if you would like to monitor your desktop instead of your downloads, you may opt to change the source directory as follows:
```python
source_dir = f"/Users/{user}/Desktop"
```
Also, if you wanted to add a place for executables (for example) to be automatically sorted into, you may choose to add a directory as follows:
```python
exe_dir = f"/Users/{user}/Documents/Executables"
```
Upon adding such a directory, you'll need to define a new attribute for sorting, sorting method, and control branch in the third, fourth, and fifth code segments. The new code would look like:
```python
exe = [
    ".exe" # add any exentsions here you feel necessary (in quotations and comma-separated)
]
```
```python
def is_exe(file):
    return os.path.splitext(file)[1].lower() in exe
```
```python
elif (is_exe(entry)):
    shutil.move(entry, exe_dir)
    logging.info(f"Moved document file {entry} to {exe_dir}")
```
So, you can adapt these fields as you deem necessary for your convenience.

In my code, there is also a section for files to be sorted into special class directories, as they prove useful to me. Unless you are taking my exact academic program at UT Austin, it may be entirely useless to you. If you are a student, you could adapt the "classes" field within the third code section and the department codes within the fifth code section; otherwise, you might just want to delete all references. I'll show all the segments that you'll need to delete below:
```python
classes = [
    "314H", "311H", "340L", "303"
]
```
```python
def is_class(file):
    for name in classes:
        if name in os.path.splitext(file)[0]:
            return True
    return False
```
```python
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
```

### DLSort Unix Executable
This is a very simple file, it simply tells the shell to run the Python script for DLSort at a designated file location. I have not included one here, as it would (likely) not work for you at all (unless your machine happens to be set up exactly the same as mine—same user and all). You'll need to create an extensionless file (the name is arbitrary) and, within it, write the following commands:
```
#!/bin/sh
Python [insert the file path to the Python script]
```
Then, in the terminal, give the following command:
```
chmod 755 [insert the file path to the extensionless file that you just created]
```
After which, the extensionless file should turn into a Unix Executable, that—when run—will trigger the Python script (dl_sort.py).

You could also, just as easily, make a shell script by creating a file with the extension .sh; however, you will need to manually run it in the shell or configure it differently than I have here.

### Running DLSort on boot
As is, you will need to manually launch the Unix Executable every time that you want access to DLSort's capabilities. For some, this is desirable; however, there is a way to run the script on boot. Here I will detail how to do that, if that interests you.

Go to your Mac's system settings, and search for "Login Items." I've attatched a screenshot from my machine (macOS Ventura 13.4.1) below:

<img width="708" alt="Screenshot 2023-07-25 at 12 44 10 AM" src="https://github.com/migopp/DLSort/assets/128272843/0c2ce9dd-a6ed-454d-ac4b-9a80a5ffdd06">

Then, you will need to add a login item using the "+" symbol. Find the file path to your Unix Executable, and then select it and confirm. After that point, you're done, and all you need to do is restart your machine.
