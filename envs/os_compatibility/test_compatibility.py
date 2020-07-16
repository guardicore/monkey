import pytest

from envs.monkey_zoo.blackbox.island_client.monkey_island_client import \
    MonkeyIslandClient

machine_list = {
    "10.0.0.36": "centos_6",
    "10.0.0.37": "centos_7",
    "10.0.0.38": "centos_8",
    "10.0.0.42": "suse_12",
    "10.0.0.41": "suse_11",
    "10.0.0.99": "kali_2019",
    "10.0.0.86": "rhel_6",
    "10.0.0.87": "rhel_7",
    "10.0.0.88": "rhel_8",
    "10.0.0.77": "debian_7",
    "10.0.0.78": "debian_8",
    "10.0.0.79": "debian_9",
    "10.0.0.66": "oracle_6",
    "10.0.0.67": "oracle_7",
    "10.0.0.22": "ubuntu_12",
    "10.0.0.24": "ubuntu_14",
    "10.0.0.29": "ubuntu_19",
    "10.0.0.4": "windows_2003_r2_32",
    "10.0.0.5": "windows_2003",
    "10.0.0.8": "windows_2008",
    "10.0.0.6": "windows_2008_32",
    "10.0.0.12": "windows_2012",
    "10.0.0.11": "windows_2012_r2",
    "10.0.0.116": "windows_2016",
    "10.0.0.119": "windows_2019",
}


@pytest.fixture(scope='class')
def island_client(island):
    island_client_object = MonkeyIslandClient(island)
    yield island_client_object


@pytest.mark.usefixtures('island_client')
# noinspection PyUnresolvedReferences
class TestOSCompatibility(object):

    def test_os_compat(self, island_client):
        print()
        all_monkeys = island_client.get_all_monkeys_from_db()
        ips_that_communicated = []
        for monkey in all_monkeys:
            for ip in monkey['ip_addresses']:
                if ip in machine_list:
                    ips_that_communicated.append(ip)
                    break
        for ip, os in machine_list.items():
            if ip not in ips_that_communicated:
                print("{} didn't communicate to island".format(os))

        if len(ips_that_communicated) < len(machine_list):
            assert False
