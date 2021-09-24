from monkey_island.cc.services.config_schema.config_schema_per_attack_technique import (
    get_config_schema_per_attack_technique,
)

FAKE_SCHEMA = {
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
    }
}

REVERSE_FAKE_SCHEMA = {
    "T0000": {
        "Definition Type 1": ["Config Option 1", "Config Option 2"],
        "Definition Type 2": ["Config Option 5", "Config Option 6"],
    },
    "T0001": {
        "Definition Type 1": ["Config Option 1"],
        "Definition Type 2": ["Config Option 5"],
    },
}


def test_get_config_schema_per_attack_technique(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.config_schema.config_schema_per_attack_technique.SCHEMA",
        FAKE_SCHEMA,
    )
    assert get_config_schema_per_attack_technique() == REVERSE_FAKE_SCHEMA
