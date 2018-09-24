""" Generic helper functions """

import os


def ensure_dir(file_path):
    """
    Checks a directory exists.  If it doesn't - makes it.

    args
        file_path (str)
    """
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)
