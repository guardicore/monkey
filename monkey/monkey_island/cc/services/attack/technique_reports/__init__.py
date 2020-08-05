import abc
import logging

from common.utils.attack_utils import ScanStatus
from common.utils.code_utils import abstractstatic
from monkey_island.cc.database import mongo
from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations
from monkey_island.cc.services.attack.attack_config import AttackConfig

logger = logging.getLogger(__name__)


disabled_msg = "This technique has been disabled. " +\
               "You can enable it from the [configuration page](../../configure)."


class AttackTechnique(object, metaclass=abc.ABCMeta):
    """ Abstract class for ATT&CK report components """

    @property
    @abc.abstractmethod
    def unscanned_msg(self):
        """
        :return: Message that will be displayed in case attack technique was not scanned.
        """
        pass

    @property
    @abc.abstractmethod
    def scanned_msg(self):
        """
        :return: Message that will be displayed in case attack technique was scanned.
        """
        pass

    @property
    @abc.abstractmethod
    def used_msg(self):
        """
        :return: Message that will be displayed in case attack technique was used by the scanner.
        """
        pass

    @property
    @abc.abstractmethod
    def tech_id(self):
        """
        :return: Id of attack technique. E.g. T1003
        """
        pass

    @staticmethod
    @abstractstatic
    def get_report_data():
        """
        :return: Report data aggregated from the database.
        """
        pass

    @classmethod
    def technique_status(cls):
        """
        Gets the status of a certain attack technique.
        :return: ScanStatus numeric value
        """
        if not cls._is_enabled_in_config():
            return ScanStatus.DISABLED.value
        elif mongo.db.telemetry.find_one({'telem_category': 'attack',
                                          'data.status': ScanStatus.USED.value,
                                          'data.technique': cls.tech_id}):
            return ScanStatus.USED.value
        elif mongo.db.telemetry.find_one({'telem_category': 'attack',
                                          'data.status': ScanStatus.SCANNED.value,
                                          'data.technique': cls.tech_id}):
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
        return {'message': cls.get_message_by_status(status), 'status': status}

    @classmethod
    def get_message_by_status(cls, status):
        """
        Picks a message to return based on status.
        :param status: Enum from common/attack_utils.py integer value
        :return: message string
        """
        if status == ScanStatus.DISABLED.value:
            return disabled_msg
        if status == ScanStatus.UNSCANNED.value:
            return cls.unscanned_msg
        elif status == ScanStatus.SCANNED.value:
            return cls.scanned_msg
        else:
            return cls.used_msg

    @classmethod
    def technique_title(cls):
        """
        :return: techniques title. E.g. "T1110 Brute force"
        """
        return AttackConfig.get_technique(cls.tech_id)['title']

    @classmethod
    def get_tech_base_data(cls):
        """
        Gathers basic attack technique data into a dict.
        :return: dict E.g. {'message': 'Brute force used', 'status': 2, 'title': 'T1110 Brute force'}
        """
        data = {}
        status = cls.technique_status()
        title = cls.technique_title()
        data.update({'status': status,
                     'title': title,
                     'message': cls.get_message_by_status(status)})
        data.update(cls.get_mitigation_by_status(status))
        return data

    @classmethod
    def get_base_data_by_status(cls, status):
        data = cls.get_message_and_status(status)
        data.update({'title': cls.technique_title()})
        data.update(cls.get_mitigation_by_status(status))
        return data

    @classmethod
    def get_mitigation_by_status(cls, status: ScanStatus) -> dict:
        if status == ScanStatus.USED.value:
            mitigation_document = AttackMitigations.get_mitigation_by_technique_id(str(cls.tech_id))
            return {'mitigations': mitigation_document.to_mongo().to_dict()['mitigations']}
        else:
            return {}

    @classmethod
    def is_status_disabled(cls, get_technique_status_and_data) -> bool:
        def check_if_disabled_in_config():
            return (ScanStatus.DISABLED.value, []) if not cls._is_enabled_in_config() else get_technique_status_and_data()
        return check_if_disabled_in_config

    @classmethod
    def _is_enabled_in_config(cls) -> bool:
        return AttackConfig.get_technique_values()[cls.tech_id]
