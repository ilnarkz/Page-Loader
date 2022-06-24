import logging
import os

from page_loader.known_error import KnownError
from page_loader.naming import get_dir_name


def create_directory(file_path: str) -> str:
    dir_for_files = get_dir_name(file_path)
    try:
        os.mkdir(dir_for_files)
    except OSError as err:
        logging.error(f"Can't create directory {dir_for_files}. Directory already exists")
        raise KnownError() from err
    return dir_for_files
