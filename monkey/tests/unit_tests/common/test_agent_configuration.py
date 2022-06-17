from common import OperatingSystems
from common.configuration import (
    CustomPBAConfigurationSchema,
    ExploitationConfiguration,
    ExploitationConfigurationSchema,
    ExploitationOptionsConfigurationSchema,
    ExploiterConfigurationSchema,
    ICMPScanConfigurationSchema,
    PluginConfigurationSchema,
    TCPScanConfigurationSchema,
)


def test_build_plugin_configuration():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
    schema = PluginConfigurationSchema()

    config = schema.load({"name": name, "options": options})

    assert config.name == name
    assert config.options == options


def test_custom_pba_configuration_schema():
    linux_command = "a"
    linux_filename = "b"
    windows_command = "c"
    windows_filename = "d"
    schema = CustomPBAConfigurationSchema()

    config = schema.load(
        {
            "linux_command": linux_command,
            "linux_filename": linux_filename,
            "windows_command": windows_command,
            "windows_filename": windows_filename,
        }
    )

    assert config.linux_command == linux_command
    assert config.linux_filename == linux_filename
    assert config.windows_command == windows_command
    assert config.windows_filename == windows_filename


def test_exploitation_options_configuration_schema():
    ports = [1, 2, 3]
    schema = ExploitationOptionsConfigurationSchema()

    config = schema.load({"http_ports": ports})

    assert config.http_ports == ports


def test_exploiter_configuration_schema():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
    supported_os = [OperatingSystems.LINUX, OperatingSystems.WINDOWS]
    schema = ExploiterConfigurationSchema()

    config = schema.load(
        {"name": name, "options": options, "supported_os": [os_.name for os_ in supported_os]}
    )

    assert config.name == name
    assert config.options == options
    assert config.supported_os == supported_os


def test_exploitation_configuration():
    ports = [1, 2, 3]
    brute_force = [
        {"name": "ex1", "options": {}, "supported_os": ["LINUX"]},
        {
            "name": "ex2",
            "options": {"smb_download_timeout": 10},
            "supported_os": ["LINUX", "WINDOWS"],
        },
    ]
    vulnerability = [
        {
            "name": "ex3",
            "options": {"smb_download_timeout": 10},
            "supported_os": ["WINDOWS"],
        },
    ]
    exploitation_config = {
        "options": {"http_ports": ports},
        "brute_force": brute_force,
        "vulnerability": vulnerability,
    }
    schema = ExploitationConfigurationSchema()

    config = schema.load(exploitation_config)
    config_dict = schema.dump(config)

    assert isinstance(config, ExploitationConfiguration)
    assert config_dict == exploitation_config


def test_icmp_scan_configuration_schema():
    timeout_ms = 2525
    schema = ICMPScanConfigurationSchema()

    config = schema.load({"timeout_ms": timeout_ms})

    assert config.timeout_ms == timeout_ms


def test_tcp_scan_configuration_schema():
    timeout_ms = 2525
    ports = [8080, 443]
    schema = TCPScanConfigurationSchema()

    config = schema.load({"timeout_ms": timeout_ms, "ports": ports})

    assert config.timeout_ms == timeout_ms
    assert config.ports == ports
