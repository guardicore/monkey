import json
import platform
from socket import gethostname
from typing import Any, Mapping
from uuid import getnode

from common import OperatingSystem
from common.network.network_utils import get_network_interfaces
from common.types import JSONSerializable
from monkey_island.cc.models import Machine

from . import IMachineRepository, StorageError, UnknownRecordError


def initialize_machine_repository(machine_repository: IMachineRepository):
    """
    Populate an IMachineRepository with island machine data

    If the island is not already present in the IMachineRepository, add it.

    :param machine_repository: The repository to populate
    :raises StorageError: If an error occurs while attempting to store data in the repository
    """
    hardware_id = getnode()

    try:
        machine_repository.get_machine_by_hardware_id(hardware_id)
    except UnknownRecordError:
        machine = Machine(
            id=machine_repository.get_new_id(),
            hardware_id=hardware_id,
            island=True,
            network_interfaces=get_network_interfaces(),
            operating_system=OperatingSystem(platform.system().lower()),
            operating_system_version=platform.version(),
            hostname=gethostname(),
        )
        machine_repository.upsert_machine(machine)


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
