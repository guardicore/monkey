import pytest

from monkey_island.cc.services.config import ConfigService

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


@pytest.fixture(scope="function", autouse=True)
def mock_port(monkeypatch, PORT):
    monkeypatch.setattr("monkey_island.cc.services.config.ISLAND_PORT", PORT)


@pytest.mark.slow
@pytest.mark.usefixtures("uses_encryptor")
def test_set_server_ips_in_config_command_servers(config, IPS, PORT):
    ConfigService.set_server_ips_in_config(config)
    expected_config_command_servers = [f"{ip}:{PORT}" for ip in IPS]
    assert config["internal"]["island_server"]["command_servers"] == expected_config_command_servers


@pytest.mark.slow
@pytest.mark.usefixtures("uses_encryptor")
def test_set_server_ips_in_config_current_server(config, IPS, PORT):
    ConfigService.set_server_ips_in_config(config)
    expected_config_current_server = f"{IPS[0]}:{PORT}"
    assert config["internal"]["island_server"]["current_server"] == expected_config_current_server


def test_format_config_for_agent__credentials_removed(flat_monkey_config):
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "exploit_lm_hash_list" not in flat_monkey_config
    assert "exploit_ntlm_hash_list" not in flat_monkey_config
    assert "exploit_password_list" not in flat_monkey_config
    assert "exploit_ssh_keys" not in flat_monkey_config
    assert "exploit_user_list" not in flat_monkey_config


def test_format_config_for_agent__ransomware_payload(flat_monkey_config):
    expected_ransomware_options = {
        "ransomware": {
            "encryption": {
                "enabled": True,
                "directories": {
                    "linux_target_dir": "/tmp/ransomware-target",
                    "windows_target_dir": "C:\\windows\\temp\\ransomware-target",
                },
            },
            "other_behaviors": {"readme": True},
        }
    }

    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "payloads" in flat_monkey_config
    assert flat_monkey_config["payloads"] == expected_ransomware_options

    assert "ransomware" not in flat_monkey_config


def test_format_config_for_agent__pbas(flat_monkey_config):
    expected_pbas_config = {
        "CommunicateAsBackdoorUser": {},
        "ModifyShellStartupFiles": {},
        "ScheduleJobs": {},
        "Timestomping": {},
        "AccountDiscovery": {},
    }
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "post_breach_actions" in flat_monkey_config
    assert flat_monkey_config["post_breach_actions"] == expected_pbas_config

    assert "custom_PBA_linux_cmd" not in flat_monkey_config
    assert "PBA_linux_filename" not in flat_monkey_config
    assert "custom_PBA_windows_cmd" not in flat_monkey_config
    assert "PBA_windows_filename" not in flat_monkey_config


def test_format_config_for_custom_pbas(flat_monkey_config):
    custom_config = {
        "linux_command": "bash test.sh",
        "windows_command": "powershell test.ps1",
        "linux_filename": "test.sh",
        "windows_filename": "test.ps1",
        "current_server": "10.197.94.72:5000",
    }
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

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


def test_format_config_for_agent__propagation(flat_monkey_config):
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "propagation" in flat_monkey_config
    assert "targets" in flat_monkey_config["propagation"]
    assert "network_scan" in flat_monkey_config["propagation"]
    assert "exploiters" in flat_monkey_config["propagation"]


def test_format_config_for_agent__propagation_targets(flat_monkey_config):
    expected_targets = {
        "blocked_ips": ["192.168.1.1", "192.168.1.100"],
        "inaccessible_subnets": ["10.0.0.0/24", "10.0.10.0/24"],
        "local_network_scan": True,
        "subnet_scan_list": ["192.168.1.50", "192.168.56.0/24", "10.0.33.0/30"],
    }

    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert flat_monkey_config["propagation"]["targets"] == expected_targets
    assert "blocked_ips" not in flat_monkey_config
    assert "inaccessible_subnets" not in flat_monkey_config
    assert "local_network_scan" not in flat_monkey_config
    assert "subnet_scan_list" not in flat_monkey_config


def test_format_config_for_agent__network_scan(flat_monkey_config):
    expected_network_scan_config = {
        "tcp": {
            "timeout_ms": 3000,
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
            "timeout_ms": 1000,
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
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "propagation" in flat_monkey_config
    assert "network_scan" in flat_monkey_config["propagation"]
    assert flat_monkey_config["propagation"]["network_scan"] == expected_network_scan_config

    assert "tcp_scan_timeout" not in flat_monkey_config
    assert "tcp_target_ports" not in flat_monkey_config
    assert "ping_scan_timeout" not in flat_monkey_config
    assert "finger_classes" not in flat_monkey_config


def test_format_config_for_agent__exploiters(flat_monkey_config):
    expected_exploiters_config = {
        "options": {
            "dropper_target_path_linux": "/tmp/monkey",
            "dropper_target_path_win_64": r"C:\Windows\temp\monkey64.exe",
            "http_ports": [80, 443, 7001, 8008, 8080, 9200],
        },
        "brute_force": [
            {"name": "MSSQLExploiter", "supported_os": ["windows"], "options": {}},
            {"name": "PowerShellExploiter", "supported_os": ["windows"], "options": {}},
            {"name": "SSHExploiter", "supported_os": ["linux"], "options": {}},
            {
                "name": "SmbExploiter",
                "supported_os": ["windows"],
                "options": {"smb_download_timeout": 300},
            },
            {
                "name": "WmiExploiter",
                "supported_os": ["windows"],
                "options": {"smb_download_timeout": 300},
            },
        ],
        "vulnerability": [
            {"name": "HadoopExploiter", "supported_os": ["linux", "windows"], "options": {}},
            {"name": "Log4ShellExploiter", "supported_os": ["linux", "windows"], "options": {}},
            {"name": "ZerologonExploiter", "supported_os": ["windows"], "options": {}},
        ],
    }
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "propagation" in flat_monkey_config
    assert "exploiters" in flat_monkey_config["propagation"]

    assert flat_monkey_config["propagation"]["exploiters"] == expected_exploiters_config
    assert "exploiter_classes" not in flat_monkey_config
