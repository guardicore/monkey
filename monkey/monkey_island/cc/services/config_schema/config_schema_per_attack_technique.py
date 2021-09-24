from typing import Dict, List

from monkey_island.cc.services.config_schema.config_schema import SCHEMA


def get_config_schema_per_attack_technique() -> Dict[str, Dict[str, List[str]]]:
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

    definitions = SCHEMA["definitions"]
    for definition in definitions:
        definition_type = definitions[definition]["title"]
        for field in definitions[definition]["anyOf"]:
            config_field = field["title"]
            for attack_technique in field.get("attack_techniques", []):
                _add_config_field_to_reverse_schema(
                    definition_type, config_field, attack_technique, reverse_schema
                )

    return reverse_schema


def _add_config_field_to_reverse_schema(
    definition_type: str, config_field: str, attack_technique: str, reverse_schema: Dict
) -> None:
    if attack_technique in reverse_schema:
        technique = reverse_schema[attack_technique]
        if definition_type in technique:
            technique[definition_type].append(config_field)
        else:
            technique[definition_type] = [config_field]
    else:
        reverse_schema[attack_technique] = {definition_type: [config_field]}


CONFIG_SCHEMA_PER_ATTACK_TECHNIQUE = get_config_schema_per_attack_technique()
