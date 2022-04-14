import abc
import logging
from typing import Dict, List

from common.utils.attack_utils import ScanStatus
from common.utils.code_utils import abstractstatic
from monkey_island.cc.database import mongo
from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations
from monkey_island.cc.services.config_schema.config_schema import SCHEMA
from monkey_island.cc.services.attack.attack_schema import SCHEMA as ATTACK_SCHEMA
from monkey_island.cc.services.config_schema.config_schema_per_attack_technique import (
    ConfigSchemaPerAttackTechnique,
)

logger = logging.getLogger(__name__)


class AttackTechnique(object, metaclass=abc.ABCMeta):
    """Abstract class for ATT&CK report components"""

    config_schema_per_attack_technique = None

    @property
    @abc.abstractmethod
    def unscanned_msg(self):
        """
        :return: Message that will be displayed in case attack technique was not scanned.
        """
        ...

    @property
    @abc.abstractmethod
    def scanned_msg(self):
        """
        :return: Message that will be displayed in case attack technique was scanned.
        """
        ...

    @property
    @abc.abstractmethod
    def used_msg(self):
        """
        :return: Message that will be displayed in case attack technique was used by the scanner.
        """
        ...

    @property
    @abc.abstractmethod
    def tech_id(self):
        """
        :return: Id of attack technique. E.g. T1003
        """
        ...

    @property
    @abc.abstractmethod
    def relevant_systems(self) -> List[str]:
        """
        :return: systems on which the technique is relevant
                 (examples: 1. "Trap Command" PBA (technique T1154) is Linux only.
                            2. "Job Scheduling" PBA has different techniques for Windows and Linux.
        """
        ...

    @staticmethod
    @abstractstatic
    def get_report_data():
        """
        :return: Report data aggregated from the database.
        """
        ...

    @classmethod
    def technique_status(cls):
        """
        Gets the status of a certain attack technique.
        :return: ScanStatus numeric value
        """
        if mongo.db.telemetry.find_one(
            {
                "telem_category": "attack",
                "data.status": ScanStatus.USED.value,
                "data.technique": cls.tech_id,
            }
        ):
            return ScanStatus.USED.value
        elif mongo.db.telemetry.find_one(
            {
                "telem_category": "attack",
                "data.status": ScanStatus.SCANNED.value,
                "data.technique": cls.tech_id,
            }
        ):
            return ScanStatus.SCANNED.value
        else:
            return ScanStatus.UNSCANNED.value

    @classmethod
    def get_message_and_status(cls, status):
        """
        Returns a dict with attack technique's message and status.
        :param status: Enum from common/attack_utils.py integer value
        :return: Dict with message and status
        """
        return {"message": cls.get_message_by_status(status), "status": status}

    @classmethod
    def get_message_by_status(cls, status):
        """
        Picks a message to return based on status.
        :param status: Enum from common/attack_utils.py integer value
        :return: message string
        """
        if status == ScanStatus.UNSCANNED.value:
            if not cls.config_schema_per_attack_technique:
                cls.config_schema_per_attack_technique = (
                    ConfigSchemaPerAttackTechnique().get_config_schema_per_attack_technique(SCHEMA)
                )
            unscanned_msg = cls._get_unscanned_msg_with_reasons(
                cls.unscanned_msg, cls.config_schema_per_attack_technique
            )
            return unscanned_msg
        elif status == ScanStatus.SCANNED.value:
            return cls.scanned_msg
        else:
            return cls.used_msg

    @classmethod
    def _get_unscanned_msg_with_reasons(
        cls, unscanned_msg: str, config_schema_per_attack_technique: Dict
    ):
        reasons = []
        if len(cls.relevant_systems) == 1:
            reasons.append(f"- Monkey did not run on any {cls.relevant_systems[0]} systems.")
        if cls.tech_id in config_schema_per_attack_technique:
            reasons.append(
                "- The following configuration options were disabled or empty:<br/>"
                f"{cls._get_relevant_config_values(config_schema_per_attack_technique)}"
            )

        if reasons:
            unscanned_msg = (
                unscanned_msg.strip(".")
                + " due to one of the following reasons:\n"
                + "\n".join(reasons)
            )

        return unscanned_msg

    @classmethod
    def _get_relevant_config_values(cls, config_schema_per_attack_technique: Dict):
        config_options = ""
        for config_type in config_schema_per_attack_technique[cls.tech_id]:
            config_options += (
                f"- {config_type} — "
                f"{', '.join(config_schema_per_attack_technique[cls.tech_id][config_type])}<br/>"
            )

        return config_options

    @classmethod
    def technique_title(cls):
        """
        :return: techniques title. E.g. "T1110 Brute force"
        """
        return get_technique(cls.tech_id)["title"]

    @classmethod
    def get_tech_base_data(cls):
        """
        Gathers basic attack technique data into a dict.
        :return: dict E.g. {'message': 'Brute force used', 'status': 2, 'title': 'T1110 Brute
        force'}
        """
        data = {}
        status = cls.technique_status()
        title = cls.technique_title()
        data.update(
            {"status": status, "title": title, "message": cls.get_message_by_status(status)}
        )
        data.update(cls.get_mitigation_by_status(status))
        return data

    @classmethod
    def get_base_data_by_status(cls, status):
        data = cls.get_message_and_status(status)
        data.update({"title": cls.technique_title()})
        data.update(cls.get_mitigation_by_status(status))
        return data

    @classmethod
    def get_mitigation_by_status(cls, status: ScanStatus) -> dict:
        if status == ScanStatus.USED.value:
            mitigation_document = AttackMitigations.get_mitigation_by_technique_id(str(cls.tech_id))
            return {"mitigations": mitigation_document.to_mongo().to_dict()["mitigations"]}
        else:
            return {}


def get_technique(technique_id):
    """
    Gets technique by id
    :param technique_id: E.g. T1210
    :return: Technique object or None if technique is not found
    """
    attack_config = ATTACK_SCHEMA["properties"]
    for config_key, attack_type in list(attack_config.items()):
        for type_key, technique in list(attack_type["properties"].items()):
            if type_key == technique_id:
                return technique
    return None
