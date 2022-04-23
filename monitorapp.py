""" Problem Reduction of MonitorApp"""
""" 13/12/2021 Anthony Mujica"""

" This program log  changes in current directory "

import os
import time
from typing import List, Tuple
from datetime import datetime

cwd: str = os.getcwd()  # current working directory -cwd

deleted = None
added = None
modified_f = list()


def list_content(path: str = ".") -> List[str]:
    content: List[str] = os.listdir(path)  # content of path given
    return content


def get_files_in_dir(content: List[str]):
    files: List[str] = []  # List of name of files in cwd
    for f in content:
        if os.path.isfile(f):
            files.append(f)

    return files


def get_dirs(content: List[str]) -> object:
    dirs: List[str] = []  # List of name of directories in cwd
    for f in content:
        if os.path.isdir(f):
            dirs.append(f)
    return dirs


def get_links(content: List[str]):
    links: List[str] = []
    for f in content:
        if os.path.islink(f):
            links.append(f)
    return links


def get_files_paths(content: List[str]):
    files_path = List[str] = []
    for f in content:
        file_path = os.path.join(cwd, f)
        files_path.append(file_path)
    return files_path


def classify_files(content: List[str]):
    files = get_files_in_dir(content)
    dirs = get_dirs(content)

    return files, dirs


def get_mtime(files: List[str]) -> List[float]:
    modified: List[float] = []
    for f in files:
        file_path = os.path.join(cwd, f)
        mtime: float = os.path.getmtime(file_path)
        modified.append(mtime)

    return modified


def check_dir(cdir: str = "."):
    fs, dirs = classify_files(list_content())
    modified = get_mtime(fs)
    return fs, dirs, modified


def to_set(previos, current) -> Tuple[set, set]:
    previous = set(previos)
    current = set(current)
    return previous, current


def difference(previous, current) -> set:
    df = current.symmetric_difference(previous)
    return df


def transform(previous, current):
    previous_set, current_set = to_set(previous, current)
    differences = difference(previous_set, current_set)
    return differences, previous_set, current_set


def notify(differences: set, previous_set: set):
    """

    @type differences: object
    """
    global deleted
    global added

    if differences.issubset(previous_set):
        deleted = differences
        message = f"{datetime.today().strftime('%d-%m-%Y %H:%M:%S')} deleted : {deleted} \n"
        print(message)
        save_log(message)

    elif not differences.issubset(previous_set):  # added files
        added = differences
        message = f"{datetime.today().strftime('%d-%m-%Y %H:%M:%S')} added : {added} \n"
        print(message)
        save_log(message)


def get_changed(previous, current):
    differences, previous_set, current_set = transform(previous, current)

    return differences, previous_set


def save_log(message):
    with open('dirlog.txt', 'a') as log:
        log.write(message)


def main():
    while True:

        files, dirs, mtime = check_dir()  # previos status of directory

        time.sleep(8)  # timeout

        current_files, current_dirs, current_mtime = check_dir()  # current status of directory

        if current_files != files:
            df, previus_set = get_changed(files, current_files)
            notify(df, previus_set)

        if current_dirs != dirs:
            df, previus_set = get_changed(dirs, current_dirs)
            notify(df, previus_set)

        if current_mtime != mtime:

            global modified_f
            if len(current_mtime) > len(mtime) or (len(current_mtime) < len(mtime)):
                pass
            else:

                for i, f in enumerate(current_mtime):  # get values modified
                    if (f not in mtime) and (i <= len(mtime) - 1):
                        modified_f.append(files[i])
                        message = f"{datetime.today().strftime('%d-%m-%Y %H:%M:%S')} modified : {modified_f[-1]} \n"
                        print(message)
                        save_log(message)


if __name__ == '__main__':
    main()
