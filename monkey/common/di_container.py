import inspect
from typing import Any, MutableMapping, Type, TypeVar

T = TypeVar("T")


class DIContainer:
    """
    A dependency injection (DI) container that uses type annotations to resolve and inject
    dependencies.
    """

    def __init__(self):
        self._type_registry = {}
        self._instance_registry = {}

    def register(self, interface: Type[T], concrete_type: Type[T]):
        """
        Register a concrete type that satisfies a given interface.

        :param interface: An interface or abstract base class that other classes depend upon
        :param concrete_type: A type (class) that implements `interface`
        """
        self._type_registry[interface] = concrete_type
        DIContainer._del_key(self._instance_registry, interface)

    def register_instance(self, interface: Type[T], instance: T):
        """
        Register a concrete instance that satisfies a given interface.

        :param interface: An interface or abstract base class that other classes depend upon
        :param instance: An instance (object) of a type that implements `interface`
        """
        self._instance_registry[interface] = instance
        DIContainer._del_key(self._type_registry, interface)

    def resolve(self, type_: Type[T]) -> T:
        """
        Resolves all dependencies and returns a new instance of `type_` using constructor dependency
        injection. Note that only positional arguments are resolved. Varargs, keyword-only args, and
        default values are ignored.

        :param type_: A type (class) to construct.
        :return: An instance of `type_`
        """
        try:
            return self._resolve_type(type_)
        except ValueError:
            pass

        args = []

        for arg_type in inspect.getfullargspec(type_).annotations.values():
            instance = self._resolve_type(arg_type)
            args.append(instance)

        return type_(*args)

    def _resolve_type(self, type_: Type[T]) -> T:
        if type_ in self._type_registry:
            return self._construct_new_instance(type_)
        elif type_ in self._instance_registry:
            return self._retrieve_registered_instance(type_)

        raise ValueError(f'Failed to resolve unknown type "{type_.__name__}"')

    def _construct_new_instance(self, arg_type: Type[T]) -> T:
        try:
            return self._type_registry[arg_type]()
        except TypeError:
            # arg_type has dependencies that must be resolved. Recursively call resolve() to
            # construct an instance of arg_type with all of the requesite dependencies injected.
            return self.resolve(self._type_registry[arg_type])

    def _retrieve_registered_instance(self, arg_type: Type[T]) -> T:
        return self._instance_registry[arg_type]

    def release(self, interface: Type[T]):
        """
        Deregister's an interface

        :param interface: The interface to release
        """
        DIContainer._del_key(self._type_registry, interface)
        DIContainer._del_key(self._instance_registry, interface)

    @staticmethod
    def _del_key(mapping: MutableMapping[T, Any], key: T):
        """
        Deletes key from mapping. Unlike the `del` keyword, this function does not raise a KeyError
        if the key does not exist.

        :param MutableMapping: A mapping from which a key will be deleted
        :param key: A key to delete from `mapping`
        """
        try:
            del mapping[key]
        except KeyError:
            pass
