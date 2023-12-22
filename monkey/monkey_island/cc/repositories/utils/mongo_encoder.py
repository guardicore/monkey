import json
from typing import Any, Mapping

from monkeytypes import JSONSerializable

from monkey_island.cc.repositories import StorageError

DOT_REPLACEMENT = "_D0T_"


def mongo_dot_encoder(serializable_input: JSONSerializable) -> JSONSerializable:
    """
    Mongo can't store keys with "." symbols (like IP's and filenames). This method
    replaces all occurrences of "." with the contents of DOT_REPLACEMENT
    :param serializable_input: Mapping to be converted to mongo compatible mapping
    :return: Mongo compatible mapping
    """
    mapping_json = json.dumps(serializable_input)
    if DOT_REPLACEMENT in mapping_json:
        raise StorageError(
            f"Mapping {serializable_input} already contains {DOT_REPLACEMENT}."
            f" Aborting the encoding procedure"
        )
    encoded_json = mapping_json.replace(".", DOT_REPLACEMENT)
    return json.loads(encoded_json)


def mongo_dot_decoder(mapping: Mapping[str, Any]):
    """
    Mongo can't store keys with "." symbols (like IP's and filenames). This method
    reverts changes made by "mongo_dot_encoder" by replacing all occurrences of DOT_REPLACEMENT
    with "."
    :param mapping: Mapping to be converted from mongo compatible mapping to original mapping
    :return: Original mapping
    """
    report_as_json = json.dumps(mapping).replace(DOT_REPLACEMENT, ".")
    return json.loads(report_as_json)
