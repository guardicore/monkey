import pytest

from infection_monkey.telemetry.base_telem import BaseTelem


@pytest.fixture(scope="package")
def TestTelem():
    class InnerTestTelem(BaseTelem):
        telem_category = None
        __test__ = False

        def __init__(self):
            pass

        def get_data(self):
            return {}

    return InnerTestTelem
