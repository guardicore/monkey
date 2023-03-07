import inspect
from contextlib import suppress
from typing import Any, Sequence, Type, TypeVar, no_type_check

from common.utils.code_utils import del_key

T = TypeVar("T")


class UnresolvableDependencyError(ValueError):
    pass


class UnregisteredConventionError(ValueError):
    pass


# Mypy doesn't handle cases where abstract class is passed as Type[...]
# https://github.com/python/mypy/issues/4717
# We are using typing.no_type_check to mitigate these errors
class DIContainer:
    """
    A dependency injection (DI) container that uses type annotations to resolve and inject
    dependencies.
    """

    def __init__(self):
        self._type_registry = {}
        self._instance_registry = {}
        self._convention_registry = {}

    @no_type_check
    def register(self, interface: Type[T], concrete_type: Type[T]):
        """
        Register a concrete `type` that satisfies a given interface.

        :param interface: An interface or abstract base class that other classes depend upon
        :param concrete_type: A `type` (class) that implements `interface`
        :raises TypeError: If `concrete_type` is not a class, or not a subclass of `interface`
        """
        if not inspect.isclass(concrete_type):
            # Ignoring arg-type error because this if clause discovers that concrete_type is not the
            # type that mypy expects.
            formatted_type_name = DIContainer._format_type_name(
                concrete_type.__class__  # type: ignore[arg-type]
            )
            raise TypeError(
                "Expected a class, but received an instance of type "
                f'"{formatted_type_name}"; Pass a class, not an instance, to register(), or use'
                "register_instance() instead"
            )

        if not issubclass(concrete_type, interface):
            raise TypeError(
                f'Class "{DIContainer._format_type_name(concrete_type)}" is not a subclass of '
                f"{DIContainer._format_type_name(interface)}"
            )

        self._type_registry[interface] = concrete_type
        del_key(self._instance_registry, interface)

    @no_type_check
    def register_instance(self, interface: Type[T], instance: T):
        """
        Register a concrete instance that satisfies a given interface.

        :param interface: An interface or abstract base class that other classes depend upon
        :param instance: An instance (object) of a `type` that implements `interface`
        :raises TypeError: If `instance` is not an instance of `interface`
        """
        if not isinstance(instance, interface):
            raise TypeError(
                "The provided instance of type "
                f'"{DIContainer._format_type_name(instance.__class__)}" '
                f"is not an instance of {DIContainer._format_type_name(interface)}"
            )

        self._instance_registry[interface] = instance
        del_key(self._type_registry, interface)

    @no_type_check
    def register_convention(self, type_: Type[T], name: str, instance: T):
        """
        Register an instance as a convention

        At times — particularly when dealing with primitive types — it can be useful to define a
        convention for how dependencies should be resolved. For example, you might want any class
        that specifies `hostname: str` in its constructor to receive the hostname of the system it's
        running on. Registering a convention allows you to assign an object instance to a type, name
        pair.

        Example:
            class TestClass:
                def __init__(self, hostname: str):
                    self.hostname = hostname

            di_container = DIContainer()
            di_container.register_convention(str, "hostname", "my_hostname.domain")

            test = di_container.resolve(TestClass)
            assert test.hostname == "my_hostname.domain"

        :param **type_**: The `type` (class) of the dependency
        :param name: The name of the dependency parameter
        :param instance: An instance (object) of `type_` that will be injected into constructors
                         that specify `[name]: [type_]` as parameters
        """
        self._convention_registry[(type_, name)] = instance

    @no_type_check
    def resolve(self, type_: Type[T]) -> T:
        """
        Resolves all dependencies and returns a new instance of `type_` using constructor dependency
        injection. Note that only positional arguments or arguments with defaults are resolved.
        Varargs and keyword-only args are ignored.

        Dependencies are resolved with the following precedence

        1. Conventions
        2. Types, Instances

        :param **type_**: A `type` (class) to construct
        :return: An instance of **type_**
        :raises UnresolvableDependencyError: If any dependencies could not be successfully resolved
        """
        with suppress(UnresolvableDependencyError):
            return self._resolve_type(type_)

        args = self.resolve_dependencies(type_)
        return type_(*args)

    def resolve_dependencies(self, type_: Type[T]) -> Sequence[Any]:
        """
        Resolves all dependencies of `type_` and returns a Sequence of objects
        that correspond `type_`'s dependencies. Note that only positional
        arguments are resolved. Varargs, keyword-only args, and default values are ignored.

        See resolve() for information about dependency resolution precedence.

        :param **type_**: A type (class) to resolve dependencies for
        :return: An Sequence of dependencies to be injected into `type_`'s constructor
        :raises UnresolvableDependencyError: If any dependencies could not be successfully resolved
        """
        args = []

        for arg_name, arg_type in inspect.getfullargspec(type_).annotations.items():
            try:
                instance = self._resolve_convention(arg_type, arg_name)
            except UnregisteredConventionError:
                try:
                    instance = self._resolve_type(arg_type)
                except UnresolvableDependencyError as err:
                    if DIContainer._has_default_argument(type_, arg_name):
                        continue

                    raise err

            args.append(instance)

        return tuple(args)

    def _resolve_convention(self, type_: Type[T], name: str) -> T:
        convention_identifier = (type_, name)
        try:
            return self._convention_registry[convention_identifier]
        except KeyError:
            raise UnregisteredConventionError(
                f"Failed to resolve unregistered convention {convention_identifier}"
            )

    def _resolve_type(self, type_: Type[T]) -> T:
        if type_ in self._type_registry:
            return self._construct_new_instance(type_)
        elif type_ in self._instance_registry:
            return self._retrieve_registered_instance(type_)

        raise UnresolvableDependencyError(
            f'Failed to resolve unregistered type "{DIContainer._format_type_name(type)}"'
        )

    def _construct_new_instance(self, arg_type: Type[T]) -> T:
        try:
            return self._type_registry[arg_type]()
        except TypeError:
            # arg_type has dependencies that must be resolved. Recursively call resolve() to
            # construct an instance of arg_type with all of the requesite dependencies injected.
            return self.resolve(self._type_registry[arg_type])

    def _retrieve_registered_instance(self, arg_type: Type[T]) -> T:
        return self._instance_registry[arg_type]

    @staticmethod
    def _has_default_argument(type_: Type[T], arg_name: str) -> bool:
        parameters = inspect.signature(type_).parameters
        return parameters[arg_name].default is not inspect.Parameter.empty

    def release(self, interface: Type[T]):
        """
        Deregister an interface

        :param interface: The interface to release
        """
        del_key(self._type_registry, interface)
        del_key(self._instance_registry, interface)

    def release_convention(self, type_: Type[T], name: str):
        """
        Deregister a convention

        :param **type_**: The `type` (class) of the dependency
        :param name: The name of the dependency parameter
        """
        convention_identifier = (type_, name)
        del_key(self._convention_registry, convention_identifier)

    @staticmethod
    def _format_type_name(type_: Type) -> str:
        try:
            return type_.__name__
        except AttributeError:
            # Some Types, like typing.Sequence, don't have a __name__ attribute in python3.7. When
            # we upgrade to a later version of Python, this exception handler may no longer be
            # necessary.
            return str(type_)
