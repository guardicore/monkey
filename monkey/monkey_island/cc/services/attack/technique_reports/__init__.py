import abc

from monkey_island.cc.database import mongo
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.attack_config import AttackConfig
from common.utils.code_utils import abstractstatic


class AttackTechnique(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def unscanned_msg(self):
        pass

    @abc.abstractproperty
    def scanned_msg(self):
        pass

    @abc.abstractproperty
    def used_msg(self):
        pass

    @abc.abstractproperty
    def tech_id(self):
        pass

    @staticmethod
    @abstractstatic
    def get_report_data():
        pass

    @staticmethod
    def technique_status(technique):
        """
        Gets status of certain attack technique. If
        :param technique:
        :return:
        """
        if mongo.db.attack_results.find_one({'status': ScanStatus.USED.value, 'technique': technique}):
            return ScanStatus.USED
        elif mongo.db.attack_results.find_one({'status': ScanStatus.SCANNED.value, 'technique': technique}):
            return ScanStatus.SCANNED
        else:
            return ScanStatus.UNSCANNED

    @staticmethod
    def technique_title(technique):
        return AttackConfig.get_technique(technique)['title']

    @staticmethod
    def get_tech_base_data(technique):
        data = {}
        status = AttackTechnique.technique_status(technique.tech_id)
        title = AttackTechnique.technique_title(technique.tech_id)
        data.update({'status': status.name, 'title': title})
        if status == ScanStatus.UNSCANNED:
            data.update({'message': technique.unscanned_msg})
        elif status == ScanStatus.SCANNED:
            data.update({'message': technique.scanned_msg})
        else:
            data.update({'message': technique.used_msg})
        return data
