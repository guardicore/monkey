import pytest

from infection_monkey.network.tools import connect


def test_connect_raises_with_empty_list():
    with pytest.raises(ConnectionError):
        connect([])


def test_connect_raises_with_bad_data():
    with pytest.raises(ValueError):
        connect(["no-port"])
