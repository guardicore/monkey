import pytest

from common.agent_configuration.validators.ip_ranges import validate_ip, validate_subnet_range


@pytest.mark.parametrize("ip", ["192.168.56.1", "0.0.0.0"])
def test_validate_ip_valid(ip):
    validate_ip(ip)


@pytest.mark.parametrize("ip", ["1.1.1", "257.256.255.255", "1.1.1.1.1"])
def test_validate_ip_invalid(ip):
    with pytest.raises(ValueError):
        validate_ip(ip)


@pytest.mark.parametrize("ip", ["192.168.56.1", "0.0.0.0"])
def test_validate_subnet_range__ip_valid(ip):
    validate_subnet_range(ip)


@pytest.mark.parametrize("ip", ["1.1.1", "257.256.255.255", "1.1.1.1.1"])
def test_validate_subnet_range__ip_invalid(ip):
    with pytest.raises(ValueError):
        validate_subnet_range(ip)


@pytest.mark.parametrize("ip_range", ["1.1.1.1 - 2.2.2.2", "1.1.1.255-1.1.1.1"])
def test_validate_subnet_range__ip_range_valid(ip_range):
    validate_subnet_range(ip_range)


@pytest.mark.parametrize(
    "ip_range",
    [
        "1.1.1-2.2.2.2",
        "0-.1.1.1-2.2.2.2",
        "a..1.1.1-2.2.2.2",
        "257.1.1.1-2.2.2.2",
        "1.1.1.1-2.2.2.2-3.3.3.3",
    ],
)
def test_validate_subnet_range__ip_range_invalid(ip_range):
    with pytest.raises(ValueError):
        validate_subnet_range(ip_range)


@pytest.mark.parametrize("hostname", ["infection.monkey", "1nfection-Monkey", "1.1.1.1a"])
def test_validate_subnet_range__hostname_valid(hostname):
    validate_subnet_range(hostname)


@pytest.mark.parametrize(
    "hostname", ["hy&!he.host", "čili-peppers.are-hot", "one.two-", "one-.two", "one@two", ""]
)
def test_validate_subnet_range__hostname_invalid(hostname):
    with pytest.raises(ValueError):
        validate_subnet_range(hostname)


@pytest.mark.parametrize("cidr_range", ["1.1.1.1/24", "1.1.1.1/0"])
def test_validate_subnet_range__cidr_valid(cidr_range):
    validate_subnet_range(cidr_range)


@pytest.mark.parametrize("cidr_range", ["1.1.1/24", "1.1.1.1/-1", "1.1.1.1/33", "1.1.1.1/222"])
def test_validate_subnet_range__cidr_invalid(cidr_range):
    with pytest.raises(ValueError):
        validate_subnet_range(cidr_range)
