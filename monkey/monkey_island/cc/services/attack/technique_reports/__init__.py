import abc

from monkey_island.cc.database import mongo
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.attack_config import AttackConfig
from common.utils.code_utils import abstractstatic


class AttackTechnique(object):
    """ Abstract class for ATT&CK report components """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def unscanned_msg(self):
        """
        :return: Message that will be displayed in case attack technique was not scanned.
        """
        pass

    @abc.abstractproperty
    def scanned_msg(self):
        """
        :return: Message that will be displayed in case attack technique was scanned.
        """
        pass

    @abc.abstractproperty
    def used_msg(self):
        """
        :return: Message that will be displayed in case attack technique was used by the scanner.
        """
        pass

    @abc.abstractproperty
    def tech_id(self):
        """
        :return: Message that will be displayed in case of attack technique not being scanned.
        """
        pass

    @staticmethod
    @abstractstatic
    def get_report_data():
        """
        :return: Report data aggregated from the database.
        """
        pass

    @staticmethod
    def technique_status(technique):
        """
        Gets the status of a certain attack technique.
        :param technique: technique's id.
        :return: ScanStatus Enum object
        """
        if mongo.db.telemetry.find_one({'telem_category': 'attack', 'data.status': ScanStatus.USED.value, 'data.technique': technique}):
            return ScanStatus.USED
        elif mongo.db.telemetry.find_one({'telem_category': 'attack', 'data.status': ScanStatus.SCANNED.value, 'data.technique': technique}):
            return ScanStatus.SCANNED
        else:
            return ScanStatus.UNSCANNED

    @staticmethod
    def get_message_and_status(technique, status):
        return {'message': technique.get_message_by_status(technique, status), 'status': status.name}

    @staticmethod
    def get_message_by_status(technique, status):
        if status == ScanStatus.UNSCANNED:
            return technique.unscanned_msg
        elif status == ScanStatus.SCANNED:
            return technique.scanned_msg
        else:
            return technique.used_msg

    @staticmethod
    def technique_title(technique):
        """
        :param technique: Technique's id. E.g. T1110
        :return: techniques title. E.g. "T1110 Brute force"
        """
        return AttackConfig.get_technique(technique)['title']

    @staticmethod
    def get_tech_base_data(technique):
        """
        Gathers basic attack technique data into a dict.
        :param technique: Technique's id. E.g. T1110
        :return: dict E.g. {'message': 'Brute force used', 'status': 'Used', 'title': 'T1110 Brute force'}
        """
        data = {}
        status = AttackTechnique.technique_status(technique.tech_id)
        title = AttackTechnique.technique_title(technique.tech_id)
        data.update({'status': status.name,
                     'title': title,
                     'message': technique.get_message_by_status(technique, status)})
        return data
