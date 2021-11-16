from typing import Dict, List


class ConfigSchemaPerAttackTechnique:
    def __init__(self) -> None:
        self.reverse_schema = {}

    def get_config_schema_per_attack_technique(
        self, schema: Dict
    ) -> Dict[str, Dict[str, List[str]]]:
        """
        :return: dictionary mapping each attack technique to relevant config fields; example -
                {
                    "T1003": {
                        "System Info Collectors": [
                            "Mimikatz collector",
                        ]
                    }
                }
        """
        self._crawl_config_schema_definitions_for_reverse_schema(schema)
        self._crawl_config_schema_properties_for_reverse_schema(schema)

        return self.reverse_schema

    def _crawl_config_schema_definitions_for_reverse_schema(self, schema: Dict):
        definitions = schema["definitions"]
        for definition in definitions:
            definition_type = definitions[definition]["title"]
            for field in definitions[definition].get("anyOf", []):
                config_field = field["title"]
                for attack_technique in field.get("attack_techniques", []):
                    self._add_config_field_to_reverse_schema(
                        definition_type, config_field, attack_technique
                    )

    def _crawl_config_schema_properties_for_reverse_schema(self, schema: Dict):
        properties = schema["properties"]
        for prop in properties:
            property_type = properties[prop]["title"]
            for category_name in properties[prop].get("properties", []):
                category = properties[prop]["properties"][category_name]
                self._crawl_properties(
                    config_option_path=property_type,
                    config_option=category,
                )

    def _crawl_properties(self, config_option_path: str, config_option: Dict):
        config_option_path = (
            f"{config_option_path} -> {config_option['title']}"
            if "title" in config_option
            else config_option_path
        )
        for config_option_name in config_option.get("properties", []):
            new_config_option = config_option["properties"][config_option_name]
            self._check_related_attack_techniques(
                config_option_path=config_option_path,
                config_option=new_config_option,
            )

            # check for "properties" and each property's related techniques recursively;
            # the levels of nesting and where related techniques are declared won't
            # always be fixed in the config schema
            self._crawl_properties(config_option_path, new_config_option)

    def _check_related_attack_techniques(self, config_option_path: str, config_option: Dict):
        for attack_technique in config_option.get("related_attack_techniques", []):
            # No config values could be a reason that related attack techniques are left
            # unscanned. See https://github.com/guardicore/monkey/issues/1518 for more.
            config_field = config_option["title"]
            self._add_config_field_to_reverse_schema(
                config_option_path, config_field, attack_technique
            )

    def _add_config_field_to_reverse_schema(
        self, definition_type: str, config_field: str, attack_technique: str
    ) -> None:
        self.reverse_schema.setdefault(attack_technique, {})
        self.reverse_schema[attack_technique].setdefault(definition_type, [])
        self.reverse_schema[attack_technique][definition_type].append(config_field)
