import importlib
import inspect
import logging
from os.path import dirname, basename, isfile, join
import glob

from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


def get_fingerprint_files():
    """
    Gets all files under current directory(/actions)
    :return: list of all files without .py ending
    """
    files = glob.glob(join(dirname(__file__), "*.py"))
    return [basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]


def get_fingerprint_instances():
    """
    Returns the fingerprint objects according to configuration as a list
    :return: A list of HostFinger objects.
    """
    fingerprinter_objects = []
    fingerprint_files = get_fingerprint_files()
    # Go through all of files
    for file in fingerprint_files:
        # Import module from that file
        module = importlib.import_module(__package__ + '.' + file)
        # Get all classes in a module
        classes = [m[1] for m in inspect.getmembers(module, inspect.isclass)
                   if ((m[1].__module__ == module.__name__) and issubclass(m[1], HostFinger))]
        # Get object from class
        for class_object in classes:
            LOG.debug("Checking if should run Fingerprinter {}".format(class_object.__name__))
            if class_object.should_run(class_object.__name__):
                fingerprinter = class_object()
                fingerprinter_objects.append(fingerprinter)
                LOG.debug("Added fingerprinter {} to fingerprint list".format(class_object.__name__))
    return fingerprinter_objects
