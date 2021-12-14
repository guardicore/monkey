import pytest

from monkey_island.cc.services.config_manipulator import update_config_on_mode_set
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


@pytest.mark.slow
@pytest.mark.usefixtures("uses_encryptor")
def test_update_config_on_mode_set_advanced(config, monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.ConfigService.get_config", lambda: config)
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.update_config",
        lambda config_json, should_encrypt: config_json,
    )

    mode = IslandModeEnum.ADVANCED
    manipulated_config = update_config_on_mode_set(mode)
    assert manipulated_config == config


@pytest.mark.slow
@pytest.mark.usefixtures("uses_encryptor")
def test_update_config_on_mode_set_ransomware(config, monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.ConfigService.get_config", lambda: config)
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.update_config",
        lambda config_json, should_encrypt: config_json,
    )

    mode = IslandModeEnum.RANSOMWARE
    manipulated_config = update_config_on_mode_set(mode)
    assert manipulated_config["monkey"]["post_breach"]["post_breach_actions"] == []
