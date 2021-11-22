import pytest

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
                    "category_1": {
                        "title": "Category 1",
                        "properties": {
                            "config_option_1": {
                                "title": "Config Option 1",
                                "related_attack_techniques": ["T0000"],
                            },
                        },
                    },
                },
            },
            "property_type_2": {
                "title": "Property Type 2",
                "properties": {
                    "category_1": {
                        "title": "Category 1",
                        "properties": {
                            "config_option_1": {
                                "title": "Config Option 1",
                                "related_attack_techniques": ["T0000"],
                            },
                        },
                    },
                    "category_2": {
                        "title": "Category 2",
                        "properties": {
                            "config_option_1": {
                                "title": "Config Option 1",
                                "properties": {
                                    "config_option_1.1": {
                                        "title": "Config Option 1.1",
                                        "related_attack_techniques": ["T0000"],
                                    },
                                },
                            },
                            "config_option_2": {
                                "title": "Config Option 2",
                                "properties": {
                                    "config_option_2.1": {
                                        "title": "Config Option 2.1",
                                        "properties": {
                                            "config_option_2.1.1": {
                                                "title": "Config Option 2.1.1",
                                                "related_attack_techniques": ["T0000"],
                                            }
                                        },
                                        "related_attack_techniques": ["T0000"],
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
