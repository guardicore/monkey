from monkey_island.cc.services.config_schema.config_schema_per_attack_technique import (
    ConfigSchemaPerAttackTechnique,
)

REVERSE_FAKE_SCHEMA = {
    "T0000": {
        "Definition Type 1": ["Config Option 1", "Config Option 2"],
        "Definition Type 2": ["Config Option 5", "Config Option 6"],
        "Property Type 1 -> Category 1": ["Config Option 1"],
        "Property Type 2 -> Category 1": ["Config Option 1"],
        "Property Type 2 -> Category 2 -> Config Option 1": ["Config Option 1.1"],
        "Property Type 2 -> Category 2 -> Config Option 2": ["Config Option 2.1"],
        "Property Type 2 -> Category 2 -> Config Option 2 -> Config Option 2.1": [
            "Config Option 2.1.1"
        ],
    },
    "T0001": {"Definition Type 1": ["Config Option 1"], "Definition Type 2": ["Config Option 5"]},
}


def test_get_config_schema_per_attack_technique(monkeypatch, fake_schema):
    assert (
        ConfigSchemaPerAttackTechnique().get_config_schema_per_attack_technique(fake_schema)
        == REVERSE_FAKE_SCHEMA
    )
