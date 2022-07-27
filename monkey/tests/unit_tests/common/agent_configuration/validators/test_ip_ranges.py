import pytest
from marshmallow import ValidationError

from common.agent_configuration.validators.ip_ranges import validate_ip, validate_subnet_range


def test_validate_ip():
    for good_input in ["192.168.56.1", "0.0.0.0"]:
        validate_ip(good_input)

    for bad_input in ["1.1.1", "257.256.255.255", "1.1.1.1.1"]:
        with pytest.raises(ValidationError):
            validate_ip(bad_input)


def test_validate_subnet_range__ip():
    _test_subent_range(
        good_inputs=["192.168.56.1", "0.0.0.0"],
        bad_inputs=["1.1.1", "257.256.255.255", "1.1.1.1.1"],
    )


def test_validate_subnet_range__ip_range():
    _test_subent_range(
        good_inputs=["1.1.1.1 - 2.2.2.2", "1.1.1.255-1.1.1.1"],
        bad_inputs=["1.1.1-2.2.2.2", "0-.1.1.1-2.2.2.2", "a..1.1.1-2.2.2.2", "257.1.1.1-2.2.2.2"],
    )


def test_validate_subnet_range__hostname():
    _test_subent_range(
        good_inputs=["infection.monkey", "1nfection-Monkey"],
        bad_inputs=["hy&!he.host", "čili-peppers.are-hot"],
    )


def test_validate_subnet_range__cidr():
    _test_subent_range(
        good_inputs=["1.1.1.1/24", "1.1.1.1/0"],
        bad_inputs=["1.1.1/24", "1.1.1.1/-1", "1.1.1.1/33", "1.1.1.1/222"],
    )


def _test_subent_range(good_inputs, bad_inputs):
    for good_input in good_inputs:
        validate_subnet_range(good_input)

    for bad_input in bad_inputs:
        with pytest.raises(ValidationError):
            validate_subnet_range(bad_input)
