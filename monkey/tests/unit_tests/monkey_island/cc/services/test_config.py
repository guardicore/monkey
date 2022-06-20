import pytest

from monkey_island.cc.services.config import ConfigService

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


@pytest.fixture(autouse=True)
def mock_flat_config(monkeypatch, flat_monkey_config):
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.get_flat_config", lambda: flat_monkey_config
    )


def test_format_config_for_agent__credentials_removed():
    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert "exploit_lm_hash_list" not in flat_monkey_config
    assert "exploit_ntlm_hash_list" not in flat_monkey_config
    assert "exploit_password_list" not in flat_monkey_config
    assert "exploit_ssh_keys" not in flat_monkey_config
    assert "exploit_user_list" not in flat_monkey_config


def test_format_config_for_agent__ransomware_payload():
    expected_ransomware_options = {
        "encryption": {
            "enabled": True,
            "directories": {
                "linux_target_dir": "/tmp/ransomware-target",
                "windows_target_dir": "C:\\windows\\temp\\ransomware-target",
            },
        },
        "other_behaviors": {"readme": True},
    }

    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert "payloads" in flat_monkey_config
    assert flat_monkey_config["payloads"][0]["name"] == "ransomware"
    assert flat_monkey_config["payloads"][0]["options"] == expected_ransomware_options

    assert "ransomware" not in flat_monkey_config


def test_format_config_for_agent__pbas():
    expected_pbas_config = [
        {"name": "CommunicateAsBackdoorUser", "options": {}},
        {"name": "ModifyShellStartupFiles", "options": {}},
        {"name": "ScheduleJobs", "options": {}},
        {"name": "Timestomping", "options": {}},
        {"name": "AccountDiscovery", "options": {}},
    ]
    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert "post_breach_actions" in flat_monkey_config
    assert flat_monkey_config["post_breach_actions"] == expected_pbas_config

    assert "custom_PBA_linux_cmd" not in flat_monkey_config
    assert "PBA_linux_filename" not in flat_monkey_config
    assert "custom_PBA_windows_cmd" not in flat_monkey_config
    assert "PBA_windows_filename" not in flat_monkey_config


def test_format_config_for_custom_pbas():
    custom_config = {
        "linux_command": "bash test.sh",
        "windows_command": "powershell test.ps1",
        "linux_filename": "test.sh",
        "windows_filename": "test.ps1",
    }
    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert flat_monkey_config["custom_pbas"] == custom_config


def test_get_config_propagation_credentials_from_flat_config(flat_monkey_config):
    expected_creds = {
        "exploit_lm_hash_list": ["lm_hash_1", "lm_hash_2"],
        "exploit_ntlm_hash_list": ["nt_hash_1", "nt_hash_2", "nt_hash_3"],
        "exploit_password_list": ["test", "iloveyou", "12345"],
        "exploit_ssh_keys": [{"private_key": "my_private_key", "public_key": "my_public_key"}],
        "exploit_user_list": ["Administrator", "root", "user", "ubuntu"],
    }

    creds = ConfigService.get_config_propagation_credentials_from_flat_config(flat_monkey_config)
    assert creds == expected_creds


def test_format_config_for_agent__propagation():
    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert "propagation" in flat_monkey_config
    assert "network_scan" in flat_monkey_config["propagation"]
    assert "exploitation" in flat_monkey_config["propagation"]


def test_format_config_for_agent__network_scan():
    expected_network_scan_config = {
        "tcp": {
            "timeout": 3000,
            "ports": [
                22,
                80,
                135,
                443,
                445,
                2222,
                3306,
                3389,
                7001,
                8008,
                8080,
                8088,
                9200,
            ],
        },
        "icmp": {
            "timeout": 1000,
        },
        "targets": {
            "blocked_ips": ["192.168.1.1", "192.168.1.100"],
            "inaccessible_subnets": ["10.0.0.0/24", "10.0.10.0/24"],
            "local_network_scan": True,
            "subnets": ["192.168.1.50", "192.168.56.0/24", "10.0.33.0/30"],
        },
        "fingerprinters": [
            {"name": "elastic", "options": {}},
            {
                "name": "http",
                "options": {"http_ports": [80, 443, 7001, 8008, 8080, 9200]},
            },
            {"name": "mssql", "options": {}},
            {"name": "smb", "options": {}},
            {"name": "ssh", "options": {}},
        ],
    }
    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert "propagation" in flat_monkey_config
    assert "network_scan" in flat_monkey_config["propagation"]
    assert flat_monkey_config["propagation"]["network_scan"] == expected_network_scan_config

    assert "tcp_scan_timeout" not in flat_monkey_config
    assert "tcp_target_ports" not in flat_monkey_config
    assert "ping_scan_timeout" not in flat_monkey_config
    assert "finger_classes" not in flat_monkey_config


def test_format_config_for_agent__propagation_network_scan_targets():
    expected_targets = {
        "blocked_ips": ["192.168.1.1", "192.168.1.100"],
        "inaccessible_subnets": ["10.0.0.0/24", "10.0.10.0/24"],
        "local_network_scan": True,
        "subnets": ["192.168.1.50", "192.168.56.0/24", "10.0.33.0/30"],
    }

    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert flat_monkey_config["propagation"]["network_scan"]["targets"] == expected_targets
    assert "blocked_ips" not in flat_monkey_config
    assert "inaccessible_subnets" not in flat_monkey_config
    assert "local_network_scan" not in flat_monkey_config
    assert "subnet_scan_list" not in flat_monkey_config


def test_format_config_for_agent__exploiters():
    expected_exploiters_config = {
        "options": {
            "http_ports": [80, 443, 7001, 8008, 8080, 9200],
        },
        "brute_force": [
            {"name": "MSSQLExploiter", "supported_os": ["WINDOWS"], "options": {}},
            {"name": "PowerShellExploiter", "supported_os": ["WINDOWS"], "options": {}},
            {"name": "SSHExploiter", "supported_os": ["LINUX"], "options": {}},
            {
                "name": "SmbExploiter",
                "supported_os": ["WINDOWS"],
                "options": {"smb_download_timeout": 30},
            },
            {
                "name": "WmiExploiter",
                "supported_os": ["WINDOWS"],
                "options": {"smb_download_timeout": 30},
            },
        ],
        "vulnerability": [
            {"name": "HadoopExploiter", "supported_os": ["LINUX", "WINDOWS"], "options": {}},
            {"name": "Log4ShellExploiter", "supported_os": ["LINUX", "WINDOWS"], "options": {}},
            {"name": "ZerologonExploiter", "supported_os": ["WINDOWS"], "options": {}},
        ],
    }
    flat_monkey_config = ConfigService.format_flat_config_for_agent()

    assert "propagation" in flat_monkey_config
    assert "exploitation" in flat_monkey_config["propagation"]

    assert flat_monkey_config["propagation"]["exploitation"] == expected_exploiters_config
    assert "exploiter_classes" not in flat_monkey_config
