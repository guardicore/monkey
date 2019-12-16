import os
import sys

__author__ = 'itay.mizeretz'


def get_binaries_dir_path():
    """
    Gets the path to the binaries dir (files packaged in pyinstaller if it was used, infection_monkey dir otherwise)
    :return: Binaries dir path
    """
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_binary_file_path(filename):
    """
    Gets the path to a binary file
    :param filename: name of the file
    :return: Path to file
    """
    return os.path.join(get_binaries_dir_path(), filename)
