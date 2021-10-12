import pytest

from monkey_island.cc.environment import Environment
from monkey_island.cc.services.config import ConfigService


@pytest.fixture
def IPS():
    return ["0.0.0.0", "9.9.9.9"]


@pytest.fixture
def PORT():
    return 9999


@pytest.fixture
def config(monkeypatch, IPS, PORT):
    monkeypatch.setattr("monkey_island.cc.services.config.local_ip_addresses", lambda: IPS)
    monkeypatch.setattr(Environment, "_ISLAND_PORT", PORT)
    config = ConfigService.get_default_config(True)
    return config


@pytest.fixture
def fake_schema():
    return {
        "definitions": {
            "definition_type_1": {
                "title": "Definition Type 1",
                "anyOf": [
                    {
                        "title": "Config Option 1",
                        "attack_techniques": ["T0000", "T0001"],
                    },
                    {
                        "title": "Config Option 2",
                        "attack_techniques": ["T0000"],
                    },
                    {
                        "title": "Config Option 3",
                        "attack_techniques": [],
                    },
                    {
                        "title": "Config Option 4",
                    },
                ],
            },
            "definition_type_2": {
                "title": "Definition Type 2",
                "anyOf": [
                    {
                        "title": "Config Option 5",
                        "attack_techniques": ["T0000", "T0001"],
                    },
                    {
                        "title": "Config Option 6",
                        "attack_techniques": ["T0000"],
                    },
                    {
                        "title": "Config Option 7",
                        "attack_techniques": [],
                    },
                    {
                        "title": "Config Option 8",
                    },
                ],
            },
        },
        "properties": {
            "property_type_1": {
                "title": "Property Type 1",
                "properties": {
                    "tab_1": {
                        "title": "Tab 1",
                        "properties": {
                            "config_option_1": {
                                "title": "Config Option 1",
                                "related_attack_techniques": ["T0000"],
                            },
                        },
                    }
                },
            }
        },
    }
