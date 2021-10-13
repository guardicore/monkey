from typing import Dict, List


def get_config_schema_per_attack_technique(schema: Dict) -> Dict[str, Dict[str, List[str]]]:
    """
    :return: dictionary mapping each attack technique to relevant config fields; example -
            {
                "T1003": {
                    "System Info Collectors": [
                        "Mimikatz collector",
                        "Azure credential collector"
                    ]
                }
            }
    """
    reverse_schema = {}

    _crawl_config_schema_definitions_for_reverse_schema(schema, reverse_schema)
    _crawl_config_schema_properties_for_reverse_schema(schema, reverse_schema)

    return reverse_schema


def _crawl_config_schema_definitions_for_reverse_schema(schema: Dict, reverse_schema: Dict):
    definitions = schema["definitions"]
    for definition in definitions:
        definition_type = definitions[definition]["title"]
        for field in definitions[definition].get("anyOf", []):
            config_field = field["title"]
            for attack_technique in field.get("attack_techniques", []):
                _add_config_field_to_reverse_schema(
                    definition_type, config_field, attack_technique, reverse_schema
                )


def _crawl_config_schema_properties_for_reverse_schema(schema: Dict, reverse_schema: Dict):
    properties = schema["properties"]
    for prop in properties:
        property_type = properties[prop]["title"]
        for category_name in properties[prop].get("properties", []):
            category = properties[prop]["properties"][category_name]
            for config_option_name in category.get("properties", []):
                config_option = category["properties"][config_option_name]
                for attack_technique in config_option.get("related_attack_techniques", []):
                    # No config values could be a reason that related attack techniques are left
                    # unscanned. See https://github.com/guardicore/monkey/issues/1518 for more.
                    config_field = f"{config_option['title']} ({category['title']})"
                    _add_config_field_to_reverse_schema(
                        property_type, config_field, attack_technique, reverse_schema
                    )


def _add_config_field_to_reverse_schema(
    definition_type: str, config_field: str, attack_technique: str, reverse_schema: Dict
) -> None:
    reverse_schema.setdefault(attack_technique, {})
    reverse_schema[attack_technique].setdefault(definition_type, [])
    reverse_schema[attack_technique][definition_type].append(config_field)
