import logging
import threading
from typing import Dict, Tuple

from infection_monkey.i_puppet import (
    ExploiterResultData,
    FingerprintData,
    IPuppet,
    PingScanData,
    PortScanData,
    PortStatus,
    PostBreachData,
)
from infection_monkey.puppet.plugin_type import PluginType

DOT_1 = "10.0.0.1"
DOT_2 = "10.0.0.2"
DOT_3 = "10.0.0.3"
DOT_4 = "10.0.0.4"

logger = logging.getLogger()


class MockPuppet(IPuppet):
    def load_plugin(self, plugin: object, plugin_type: PluginType) -> None:
        logger.debug(f"load_plugin({plugin}, {plugin_type})")

    def run_sys_info_collector(self, name: str) -> Dict:
        logger.debug(f"run_sys_info_collector({name})")
        # TODO: More collectors
        if name == "LinuxInfoCollector":
            return {
                "credentials": {},
                "network_info": {
                    "networks": [
                        {"addr": "10.0.0.7", "netmask": "255.255.255.0"},
                        {"addr": "10.45.31.103", "netmask": "255.255.255.0"},
                        {"addr": "192.168.33.241", "netmask": "255.255.0.0"},
                    ]
                },
                "ssh_info": [
                    {
                        "name": "m0nk3y",
                        "home_dir": "/home/m0nk3y",
                        "public_key": "ssh-rsa "
                        "AAAAB3NzaC1yc2EAAAADAQABAAABAQCqhqTJfcrAbTUPzQ+Ou9bhQjmP29jRBz00BAdvNu77Y1SwM/+wETxapv7QPG55oc04Y5qR1KaItcwz3Prh7Qe/ohP/I2mIhP5tDRNfYHxXaGtj58wQhFrkrUhERVvEvwyvb97RWPAtAJjWT8+S6ASjjvyUNHulFIjJ0Yptlj2fboeh1eETDQ4FKfofpgwmab110ct2500FOtY1MWqFgpRvV0EX8WgJoscQ5FnsJAn6Ueb3DnsrIDq1LtK1rmxGSiZwpgOCwvyC1FFfHeP+cfpPsS+G9pBSYm2VqR42QL1BJL1pm4wFPVrBDmzORVQRf35k6agL7loRlfmAt28epDi1 ubuntu@test\n",  # noqa: E501
                        "private_key": "-----BEGIN RSA PRIVATE KEY-----\n"
                        "MIIEpAIBAAKCAQEAqoakyX3KwG01D80PjrvW4UI5j9vY0Qc9NAQHbzbu+2NUsDP/\n"
                        "sBE8Wqb+0DxueaHNOGOakdSmiLXMM9z64e0Hv6IT/yNpiIT+bQ0TX2B8V2hrY+fM\n"
                        "Ew0OBSn6H6YMJmm9ddHLdudNBTrWNTFqhYKUb1dBF/FoCaLHEORZ7CQJ+lHm9w57\n"
                        "KyA6tS7Sta5sRkomcKYDgsL8gtRRXx3j/nH6T7EvhvaQUmJtlakeNkC9QSS9aZuM\n"
                        "snegLvVSlHVmKe8SjD0YAF7g9HH/vm0R2jYTYSArslw4mUZMjTcAQ/XBeDHDkNZq\n"
                        "x9ECzXdeZhXCXlKcadC+kNp+yT4MwkHAjid6AyalSDJ+9k3QRaI6ItxofWJhnZdB\n"
                        "RxQtnkJNOZCMKqwxmxUweX7AyShT1KdBdkw0VzkY0O3VUgdR9IzQu73eME5Qr4LM\n"
                        "5x+rFy0EggHkzCXecviDDQ/SJZEDR4yE0SCxwY0GxVfDdvM6aoLK7wLfu0hG+hjO\n"
                        "ewXmOAECgYEA4yA14atxKYWf8tAJnmH+IJi1nuiyBoaKJh9nGulGTFVpugytkfdy\n"
                        "omGYsvlSJd6x4KPM2nXuSD9uvS0ZDeHDXbPJcFAPscghwwIekunQigECgYEAwDRl\n"
                        "QOhBx8PpicbRmoEe06zb+gRNTYTnvcHgkJN275pqTn1hIAdQSGnyuyWdCN6CU8cg\n"
                        "p7ecLbCujAstim4H8LG6xMv8jBgVeBKclKEEy9IpvMZ/DGOdUS4/RMWkdVbcFFHZ\n"
                        "57gycmFwgN7ZFXdMkuCCZi2KCa4jX54G1VNX0+k64cLV8lgQXvVyl9QdvBkt8NqB\n"
                        "Zoce2vfDrFkUHoxQmAl2jvn8925KkAdga4Zj+zvLgmcryxCFZnA6IvxaoHzrUSxO\n"
                        "HpuEdCFek/4gyhXPbYQO99ZtOjx0mXwZVqRaEA1kvhX3+PjoPRO2wgBLXVNyb+P5\n"
                        "5Bxfk6XI40UAUSYv6XQlfIQj0xz/YfSkWbOwTJOShgMbJtiZVFuZ2YcEjSYXzNtv\n"
                        "WBM0+05OGqjxdyI+qpjHqrZVWN9WvvkH0gJz+zvcorygINMnuSjpNCw4nipXHaud\n"
                        "LbiqWK42eTmVSiFH+pH+YwVaTatc0RfQ7OP218GD8dtkTgw2JFOzbA==\n"
                        "-----END RSA PRIVATE KEY-----\n",
                        "known_hosts": "|1|pERVcy3opIGJnp7HVTpeA0FmuEY=|L64j7430lwkSFrmcn49Nf8YEsLc= "  # noqa: E501
                        "ssh-rsa "
                        "AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==\n"  # noqa: E501
                        "|1|DXEyHSAtnxSSWb4z6XLaxHJL/aM=|zjIBopXOz1GB9hbdpVcYsHY+eSU= "
                        "ssh-rsa "
                        "AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==\n"  # noqa: E501
                        "10.197.94.221 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBL3o1lUn7mZ6HNKDlkFJH9lvFIOXpTH62XkxM7wKXeZbKUy1BKnx2Jkkpv6736XnbFNkUHSnPlCAYDBqsH4nr28=\n"  # noqa: E501
                        "|1|kVjsp1IWhGMsWfrbQuhLUABrNMk=|xKCh+yr8mPEyCLZ2/E5bC8bjvw0= "
                        "ecdsa-sha2-nistp256 "
                        "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBL3o1lUn7mZ6HNKDlkFJH9lvFIOXpTH62XkxM7wKXeZbKUy1BKnx2Jkkpv6736XnbFNkUHSnPlCAYDBqsH4nr28=\n"  # noqa: E501
                        "other_host,fd42:5289:fddc:ffdf:216:3eff:fe5b:9114 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBL3o1lUn7mZ6HNKDlkFJH9lvFIOXpTH62XkxM7wKXeZbKUy1BKnx2Jkkpv6736XnbFNkUHSnPlCAYDBqsH4nr28=\n"  # noqa: E501
                        "|1|S6K6SneX+l7xTM1gNLvDAAzj4gs=|cSOIX6qf5YuIe2aw/KmUrM2ye/c= "
                        "ecdsa-sha2-nistp256 "
                        "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBL3o1lUn7mZ6HNKDlkFJH9lvFIOXpTH62XkxM7wKXeZbKUy1BKnx2Jkkpv6736XnbFNkUHSnPlCAYDBqsH4nr28=\n",  # noqa: E501
                    }
                ],
            }
        if name == "ProcessListCollector":
            return {
                "process_list": {
                    1: {
                        "cmdline": "/sbin/init",
                        "full_image_path": "/sbin/init",
                        "name": "systemd",
                        "pid": 1,
                        "ppid": 0,
                    },
                    65: {
                        "cmdline": "/lib/systemd/systemd-journald",
                        "full_image_path": "/lib/systemd/systemd-journald",
                        "name": "systemd-journald",
                        "pid": 65,
                        "ppid": 1,
                    },
                    84: {
                        "cmdline": "/lib/systemd/systemd-udevd",
                        "full_image_path": "/lib/systemd/systemd-udevd",
                        "name": "systemd-udevd",
                        "pid": 84,
                        "ppid": 1,
                    },
                    192: {
                        "cmdline": "/lib/systemd/systemd-networkd",
                        "full_image_path": "/lib/systemd/systemd-networkd",
                        "name": "systemd-networkd",
                        "pid": 192,
                        "ppid": 1,
                    },
                    17749: {
                        "cmdline": "-zsh",
                        "full_image_path": "/bin/zsh",
                        "name": "zsh",
                        "pid": 17749,
                        "ppid": 17748,
                    },
                    18392: {
                        "cmdline": "/home/ubuntu/venvs/monkey/bin/python " "monkey_island.py",
                        "full_image_path": "/usr/bin/python3.7",
                        "name": "python",
                        "pid": 18392,
                        "ppid": 17502,
                    },
                    18400: {
                        "cmdline": "/home/ubuntu/git/monkey/monkey/monkey_island/bin/mongodb/bin/mongod "  # noqa:  E501
                        "--dbpath /home/ubuntu/.monkey_island/db",
                        "full_image_path": "/home/ubuntu/git/monkey/monkey/monkey_island/bin/mongodb/bin/mongod",  # noqa:  E501
                        "name": "mongod",
                        "pid": 18400,
                        "ppid": 18392,
                    },
                    26535: {
                        "cmdline": "ACCESS DENIED",
                        "full_image_path": "null",
                        "name": "null",
                        "pid": 26535,
                        "ppid": 26469,
                    },
                    29291: {
                        "cmdline": "python infection_monkey.py m0nk3y -s " "localhost:5000",
                        "full_image_path": "/usr/bin/python3.7",
                        "name": "python",
                        "pid": 29291,
                        "ppid": 17749,
                    },
                }
            }

        return {}

    def run_pba(self, name: str, options: Dict) -> PostBreachData:
        logger.debug(f"run_pba({name}, {options})")

        if name == "AccountDiscovery":
            return PostBreachData("pba command 1", ["pba result 1", True])
        else:
            return PostBreachData("pba command 2", ["pba result 2", False])

    def ping(self, host: str, timeout: float = 1) -> PingScanData:
        logger.debug(f"run_ping({host}, {timeout})")
        if host == DOT_1:
            return PingScanData(True, "windows")

        if host == DOT_2:
            return PingScanData(False, None)

        if host == DOT_3:
            return PingScanData(True, "linux")

        if host == DOT_4:
            return PingScanData(False, None)

        return PingScanData(False, None)

    def scan_tcp_port(self, host: str, port: int, timeout: int = 3) -> PortScanData:
        logger.debug(f"run_scan_tcp_port({host}, {port}, {timeout})")
        dot_1_results = {
            22: PortScanData(22, PortStatus.CLOSED, None, None),
            445: PortScanData(445, PortStatus.OPEN, "SMB BANNER", "tcp-445"),
            3389: PortScanData(3389, PortStatus.OPEN, "", "tcp-3389"),
        }
        dot_3_results = {
            22: PortScanData(22, PortStatus.OPEN, "SSH BANNER", "tcp-22"),
            443: PortScanData(443, PortStatus.OPEN, "HTTPS BANNER", "tcp-443"),
            3389: PortScanData(3389, PortStatus.CLOSED, "", None),
        }

        if host == DOT_1:
            return dot_1_results.get(port, _get_empty_results(port))

        if host == DOT_3:
            return dot_3_results.get(port, _get_empty_results(port))

        return _get_empty_results(port)

    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
    ) -> FingerprintData:
        logger.debug(f"fingerprint({name}, {host})")
        empty_fingerprint_data = FingerprintData(None, None, {})

        dot_1_results = {
            "SMBFinger": FingerprintData(
                "windows", "vista", {"tcp-445": {"name": "smb_service_name"}}
            )
        }

        dot_3_results = {
            "SSHFinger": FingerprintData(
                "linux", "ubuntu", {"tcp-22": {"name": "SSH", "banner": "SSH BANNER"}}
            ),
            "HTTPFinger": FingerprintData(
                None,
                None,
                {
                    "tcp-80": {"name": "http", "data": ("SERVER_HEADERS", False)},
                    "tcp-443": {"name": "http", "data": ("SERVER_HEADERS_2", True)},
                },
            ),
        }

        if host == DOT_1:
            return dot_1_results.get(name, empty_fingerprint_data)

        if host == DOT_3:
            return dot_3_results.get(name, empty_fingerprint_data)

        return empty_fingerprint_data

    def exploit_host(
        self, name: str, host: str, options: Dict, interrupt: threading.Event
    ) -> ExploiterResultData:
        logger.debug(f"exploit_hosts({name}, {host}, {options})")
        attempts = [
            {
                "result": False,
                "user": "Administrator",
                "password": "",
                "lm_hash": "",
                "ntlm_hash": "",
                "ssh_key": host,
            },
            {
                "result": False,
                "user": "root",
                "password": "",
                "lm_hash": "",
                "ntlm_hash": "",
                "ssh_key": host,
            },
        ]
        info_powershell = {
            "display_name": "PowerShell",
            "started": "2021-11-25T15:57:06.307696",
            "finished": "2021-11-25T15:58:33.788238",
            "vulnerable_urls": [],
            "vulnerable_ports": [],
            "executed_cmds": [
                {
                    "cmd": "/tmp/monkey m0nk3y -s 10.10.10.10:5000 -d 1 >git s /dev/null 2>&1 &",
                    "powershell": True,
                }
            ],
        }
        info_ssh = {
            "display_name": "SSH",
            "started": "2021-11-25T15:57:06.307696",
            "finished": "2021-11-25T15:58:33.788238",
            "vulnerable_urls": [],
            "vulnerable_ports": [22],
            "executed_cmds": [],
        }
        successful_exploiters = {
            DOT_1: {
                "PowerShellExploiter": ExploiterResultData(True, info_powershell, attempts, None)
            },
            DOT_3: {
                "SSHExploiter": ExploiterResultData(False, info_ssh, attempts, "Failed exploiting")
            },
        }

        return successful_exploiters[host][name]

    def run_payload(
        self, name: str, options: Dict, interrupt: threading.Event
    ) -> Tuple[None, bool, str]:
        logger.debug(f"run_payload({name}, {options})")
        return (None, True, "")

    def cleanup(self) -> None:
        print("Cleanup called!")
        pass


def _get_empty_results(port: int):
    return PortScanData(port, PortStatus.CLOSED, None, None)
