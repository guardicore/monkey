import abc

import pytest

from common import DIContainer


class IServiceA(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def do_something(self):
        pass


class IServiceB(metaclass=abc.ABCMeta):
    pass


class ServiceA(IServiceA):
    def do_something(self):
        pass


class ServiceB(IServiceB):
    pass


class TestClass1:
    __test__ = False

    def __init__(self, service_a: IServiceA):
        self.service_a = service_a


class TestClass2:
    __test__ = False

    def __init__(self, service_b: IServiceB):
        self.service_b = service_b


class TestClass3:
    __test__ = False

    def __init__(self, service_a: IServiceA, service_b: IServiceB):
        self.service_a = service_a
        self.service_b = service_b


@pytest.fixture
def container():
    return DIContainer()


def test_register_resolve(container):
    container.register(IServiceA, ServiceA)
    test_1 = container.resolve(TestClass1)

    assert isinstance(test_1.service_a, ServiceA)


def test_correct_instance_type_injected(container):
    container.register(IServiceA, ServiceA)
    container.register(IServiceB, ServiceB)
    test_1 = container.resolve(TestClass1)
    test_2 = container.resolve(TestClass2)

    assert isinstance(test_1.service_a, ServiceA)
    assert isinstance(test_2.service_b, ServiceB)


def test_multiple_correct_instance_types_injected(container):
    container.register(IServiceA, ServiceA)
    container.register(IServiceB, ServiceB)
    test_3 = container.resolve(TestClass3)

    assert isinstance(test_3.service_a, ServiceA)
    assert isinstance(test_3.service_b, ServiceB)


def test_register_instance(container):
    service_a_instance = ServiceA()

    container.register_instance(IServiceA, service_a_instance)
    test_1 = container.resolve(TestClass1)

    assert id(service_a_instance) == id(test_1.service_a)


def test_register_multiple_instances(container):
    service_a_instance = ServiceA()
    service_b_instance = ServiceB()

    container.register_instance(IServiceA, service_a_instance)
    container.register_instance(IServiceB, service_b_instance)
    test_3 = container.resolve(TestClass3)

    assert id(service_a_instance) == id(test_3.service_a)
    assert id(service_b_instance) == id(test_3.service_b)


def test_register_mixed_instance_and_type(container):
    service_a_instance = ServiceA()

    container.register_instance(IServiceA, service_a_instance)
    container.register(IServiceB, ServiceB)
    test_2 = container.resolve(TestClass2)
    test_3 = container.resolve(TestClass3)

    assert id(service_a_instance) == id(test_3.service_a)
    assert isinstance(test_2.service_b, ServiceB)
    assert isinstance(test_3.service_b, ServiceB)
    assert id(test_2.service_b) != id(test_3.service_b)


def test_unregistered_type(container):
    with pytest.raises(ValueError):
        container.resolve(TestClass1)


def test_type_registration_overwritten(container):
    class ServiceA2(IServiceA):
        def do_something(self):
            pass

    container.register(IServiceA, ServiceA)
    container.register(IServiceA, ServiceA2)
    test_1 = container.resolve(TestClass1)

    assert isinstance(test_1.service_a, ServiceA2)


def test_instance_registration_overwritten(container):
    service_a_instance_1 = ServiceA()
    service_a_instance_2 = ServiceA()

    container.register_instance(IServiceA, service_a_instance_1)
    container.register_instance(IServiceA, service_a_instance_2)
    test_1 = container.resolve(TestClass1)

    assert id(test_1.service_a) != id(service_a_instance_1)
    assert id(test_1.service_a) == id(service_a_instance_2)


def test_type_overrides_instance(container):
    service_a_instance = ServiceA()

    container.register_instance(IServiceA, service_a_instance)
    container.register(IServiceA, ServiceA)
    test_1 = container.resolve(TestClass1)

    assert id(test_1.service_a) != id(service_a_instance)
    assert isinstance(test_1.service_a, ServiceA)


def test_instance_overrides_type(container):
    service_a_instance = ServiceA()

    container.register(IServiceA, ServiceA)
    container.register_instance(IServiceA, service_a_instance)
    test_1 = container.resolve(TestClass1)

    assert id(test_1.service_a) == id(service_a_instance)


def test_release_type(container):
    container.register(IServiceA, ServiceA)
    container.release(IServiceA)

    with pytest.raises(ValueError):
        container.resolve(TestClass1)


def test_release_instance(container):
    service_a_instance = ServiceA()
    container.register_instance(IServiceA, service_a_instance)

    container.release(IServiceA)

    with pytest.raises(ValueError):
        container.resolve(TestClass1)


class IServiceC(metaclass=abc.ABCMeta):
    pass


class ServiceC(IServiceC):
    def __init__(self, service_a: IServiceA):
        self.service_a = service_a


class TestClass4:
    __test__ = False

    def __init__(self, service_c: IServiceC):
        self.service_c = service_c


def test_recursive_resolution__depth_2(container):
    service_a_instance = ServiceA()
    container.register_instance(IServiceA, service_a_instance)
    container.register(IServiceC, ServiceC)

    test4 = container.resolve(TestClass4)

    assert isinstance(test4.service_c, ServiceC)
    assert id(test4.service_c.service_a) == id(service_a_instance)


class IServiceD(metaclass=abc.ABCMeta):
    pass


class ServiceD(IServiceD):
    def __init__(self, service_c: IServiceC, service_b: IServiceB):
        self.service_b = service_b
        self.service_c = service_c


class TestClass5:
    __test__ = False

    def __init__(self, service_d: IServiceD):
        self.service_d = service_d


def test_recursive_resolution__depth_3(container):
    container.register(IServiceA, ServiceA)
    container.register(IServiceB, ServiceB)
    container.register(IServiceC, ServiceC)
    container.register(IServiceD, ServiceD)

    test5 = container.resolve(TestClass5)

    assert isinstance(test5.service_d, ServiceD)
    assert isinstance(test5.service_d.service_b, ServiceB)
    assert isinstance(test5.service_d.service_c, ServiceC)
    assert isinstance(test5.service_d.service_c.service_a, ServiceA)


def test_resolve_registered_interface(container):
    container.register(IServiceA, ServiceA)

    resolved_instance = container.resolve(IServiceA)

    assert isinstance(resolved_instance, ServiceA)


def test_resolve_registered_instance(container):
    service_a_instance = ServiceA()
    container.register_instance(IServiceA, service_a_instance)

    service_a_actual_instance = container.resolve(IServiceA)

    assert id(service_a_actual_instance) == id(service_a_instance)


def test_resolve_dependencies(container):
    container.register(IServiceA, ServiceA)
    container.register(IServiceB, ServiceB)

    dependencies = container.resolve_dependencies(TestClass3)

    assert isinstance(dependencies[0], ServiceA)
    assert isinstance(dependencies[1], ServiceB)


def test_register_instance_as_type(container):
    service_a_instance = ServiceA()
    with pytest.raises(TypeError):
        container.register(IServiceA, service_a_instance)


def test_register_conflicting_type(container):
    with pytest.raises(TypeError):
        container.register(IServiceA, ServiceB)


def test_register_instance_with_conflicting_type(container):
    service_b_instance = ServiceB()
    with pytest.raises(TypeError):
        container.register_instance(IServiceA, service_b_instance)


class TestClass6:
    __test__ = False

    def __init__(self, my_str: str):
        self.my_str = my_str


def test_register_convention(container):
    my_str = "test_string"
    container.register_convention(str, "my_str", my_str)

    test_6 = container.resolve(TestClass6)

    assert test_6.my_str == my_str


class TestClass7:
    __test__ = False

    def __init__(self, my_str1: str, my_str2: str):
        self.my_str1 = my_str1
        self.my_str2 = my_str2


def test_register_convention__multiple_parameters_same_type(container):
    my_str1 = "s1"
    my_str2 = "s2"
    container.register_convention(str, "my_str2", my_str2)
    container.register_convention(str, "my_str1", my_str1)

    test_7 = container.resolve(TestClass7)
    assert test_7.my_str1 == my_str1
    assert test_7.my_str2 == my_str2


class TestClass8:
    __test__ = False

    def __init__(self, my_str: str, my_int: int):
        self.my_str = my_str
        self.my_int = my_int


def test_register_convention__multiple_parameters_different_types(container):
    my_str = "test_string"
    my_int = 42
    container.register_convention(str, "my_str", my_str)
    container.register_convention(int, "my_int", my_int)

    test_8 = container.resolve(TestClass8)
    assert test_8.my_str == my_str
    assert test_8.my_int == my_int


class TestClass9:
    __test__ = False

    def __init__(self, service_a: IServiceA, my_str: str):
        self.service_a = service_a
        self.my_str = my_str


def test_register_convention__type_properly_resolved(container):
    my_str = "test_string"

    container.register(IServiceA, ServiceA)
    container.register_convention(str, "my_str", my_str)
    test_9 = container.resolve(TestClass9)

    assert isinstance(test_9.service_a, ServiceA)
    assert test_9.my_str == my_str


def test_register_convention__instance_properly_resolved(container):
    service_a_instance = ServiceA()
    my_str = "test_string"

    container.register_instance(IServiceA, service_a_instance)
    container.register_convention(str, "my_str", my_str)
    test_9 = container.resolve(TestClass9)

    assert id(service_a_instance) == id(test_9.service_a)
    assert test_9.my_str == my_str


def test_release_convention(container):
    my_str = "test_string"
    container.register_convention(str, "my_str", my_str)

    with pytest.raises(ValueError):
        container.release_convention(str, "my_str")
        container.resolve(TestClass6)


class Dependency:
    def __init__(self, my_int=42):
        self.my_int = my_int


class HasDefault:
    def __init__(self, dependency: Dependency = Dependency(99)):
        self.dependency = dependency


def test_handle_default_parameter__no_dependency_registered(container):
    has_default = container.resolve(HasDefault)
    assert has_default.dependency.my_int == 99


def test_handle_default_parameter__dependency_registered(container):
    container.register(Dependency, Dependency)

    has_default = container.resolve(HasDefault)
    assert has_default.dependency.my_int == 42


def test_handle_default_parameter__skip_default(container):
    class HasDefault_2_Parameters:
        def __init__(self, dependency: Dependency = Dependency(99), my_str: str = "hello"):
            self.dependency = dependency
            self.my_str = my_str

    container.register_instance(str, "goodbye")

    has_default = container.resolve(HasDefault_2_Parameters)

    assert has_default.dependency.my_int == 99
    assert has_default.my_str == "goodbye"
