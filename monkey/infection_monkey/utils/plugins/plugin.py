import glob
import importlib
import inspect
import logging
from abc import ABCMeta, abstractmethod
from os.path import basename, dirname, isfile, join
from typing import Callable, Sequence, Type, TypeVar

LOG = logging.getLogger(__name__)


def _get_candidate_files(base_package_file):
    files = glob.glob(join(dirname(base_package_file), "*.py"))
    return [basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]


PluginType = TypeVar('PluginType', bound='Plugin')


class Plugin(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def should_run(class_name: str) -> bool:
        raise NotImplementedError()

    @classmethod
    def get_classes(cls) -> Sequence[Callable]:
        """
        Returns the class objects from base_package_spec
        base_package name and file must refer to the same package otherwise bad results
        :return: A list of parent_class classes.
        """
        objects = []
        candidate_files = _get_candidate_files(cls.base_package_file())
        LOG.info("looking for classes of type {} in {}".format(cls.__name__, cls.base_package_name()))
        # Go through all of files
        for file in candidate_files:
            # Import module from that file
            module = importlib.import_module('.' + file, cls.base_package_name())
            # Get all classes in a module
            # m[1] because return object is (name,class)
            classes = [m[1] for m in inspect.getmembers(module, inspect.isclass)
                       if ((m[1].__module__ == module.__name__) and issubclass(m[1], cls))]
            # Get object from class
            for class_object in classes:
                LOG.debug("Checking if should run object {}".format(class_object.__name__))
                try:
                    if class_object.should_run(class_object.__name__):
                        objects.append(class_object)
                        LOG.debug("Added {} to list".format(class_object.__name__))
                except Exception as e:
                    LOG.warning("Exception {} when checking if {} should run".format(str(e), class_object.__name__))
        return objects

    @classmethod
    def get_instances(cls) -> Sequence[Type[PluginType]]:
        """
        Returns the type objects from base_package_spec.
        base_package name and file must refer to the same package otherwise bad results
        :return: A list of parent_class objects.
        """
        class_objects = cls.get_classes()
        instances = []
        for class_object in class_objects:
            try:
                instance = class_object()
                instances.append(instance)
            except Exception as e:
                LOG.warning("Exception {} when initializing {}".format(str(e), class_object.__name__))
        return instances

    @staticmethod
    @abstractmethod
    def base_package_file():
        pass

    @staticmethod
    @abstractmethod
    def base_package_name():
        pass
