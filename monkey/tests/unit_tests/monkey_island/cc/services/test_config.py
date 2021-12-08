import pytest

from monkey_island.cc.services.config import ConfigService

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


@pytest.fixture(scope="function", autouse=True)
def mock_port(monkeypatch, PORT):
    monkeypatch.setattr("monkey_island.cc.services.config.ISLAND_PORT", PORT)


@pytest.mark.usefixtures("uses_encryptor")
def test_set_server_ips_in_config_command_servers(config, IPS, PORT):
    ConfigService.set_server_ips_in_config(config)
    expected_config_command_servers = [f"{ip}:{PORT}" for ip in IPS]
    assert config["internal"]["island_server"]["command_servers"] == expected_config_command_servers


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
    expected_ransomware_config = {
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
    assert flat_monkey_config["payloads"] == expected_ransomware_config

    assert "ransomware" not in flat_monkey_config


def test_format_config_for_agent__pbas(flat_monkey_config):
    expected_pbas_config = {
        "CommunicateAsBackdoorUser": {},
        "ModifyShellStartupFiles": {},
        "ScheduleJobs": {},
        "Timestomping": {},
        "AccountDiscovery": {},
        "Custom": {
            "linux_command": "bash test.sh",
            "windows_command": "powershell test.ps1",
            "linux_filename": "test.sh",
            "windows_filename": "test.ps1",
        },
    }
    ConfigService.format_flat_config_for_agent(flat_monkey_config)

    assert "post_breach_actions" in flat_monkey_config
    assert flat_monkey_config["post_breach_actions"] == expected_pbas_config

    assert "custom_PBA_linux_cmd" not in flat_monkey_config
    assert "PBA_linux_filename" not in flat_monkey_config
    assert "custom_PBA_windows_cmd" not in flat_monkey_config
    assert "PBA_windows_filename" not in flat_monkey_config


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
