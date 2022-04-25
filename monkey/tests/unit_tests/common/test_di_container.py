import pytest

from common import DIContainer


class IServiceA:
    pass


class IServiceB:
    pass


class ServiceA(IServiceA):
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


def test_unregistered_type():
    container = DIContainer()
    with pytest.raises(ValueError):
        container.resolve(TestClass1)


def test_type_registration_overwritten(container):
    class ServiceA2(IServiceA):
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


def test_release_type():
    container = DIContainer()

    container.register(IServiceA, ServiceA)
    container.release(IServiceA)

    with pytest.raises(ValueError):
        container.resolve(TestClass1)


def test_release_instance():
    container = DIContainer()
    service_a_instance = ServiceA()

    container.register_instance(IServiceA, service_a_instance)
    container.release(IServiceA)

    with pytest.raises(ValueError):
        container.resolve(TestClass1)
