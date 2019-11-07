import importlib
import inspect
import logging
from os.path import dirname, basename, isfile, join
import glob

from infection_monkey.utils.plugins.plugin import Plugin

LOG = logging.getLogger(__name__)


def _get_candidate_files(base_package_file):
    files = glob.glob(join(dirname(base_package_file), "*.py"))
    return [basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]


def get_instances(base_package_name, base_package_file, parent_class: Plugin):
    """
    Returns the parent_class type objects from base_package_spec.
    parent_class must be a class object that inherits from Plugin
    base_package name and file must refer to the same package otherwise bad results
    :return: A list of parent_class objects.
    """
    objects = []
    candidate_files = _get_candidate_files(base_package_file)
    LOG.info("looking for classes of type {} in {}".format(parent_class.__name__, base_package_name))
    # Go through all of files
    for file in candidate_files:
        # Import module from that file
        module = importlib.import_module('.' + file, base_package_name)
        # Get all classes in a module
        # m[1] because return object is (name,class)
        classes = [m[1] for m in inspect.getmembers(module, inspect.isclass)
                   if ((m[1].__module__ == module.__name__) and issubclass(m[1], parent_class))]
        # Get object from class
        for class_object in classes:
            LOG.debug("Checking if should run object {}".format(class_object.__name__))
            if class_object.should_run(class_object.__name__):
                instance = class_object()
                objects.append(instance)
                LOG.debug("Added {} to list".format(class_object.__name__))
    return objects
