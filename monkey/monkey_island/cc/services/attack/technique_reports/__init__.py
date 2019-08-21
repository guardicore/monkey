import abc
import logging

from monkey_island.cc.database import mongo
from common.utils.attack_utils import ScanStatus, UsageEnum
from monkey_island.cc.services.attack.attack_config import AttackConfig
from common.utils.code_utils import abstractstatic

logger = logging.getLogger(__name__)


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

    @classmethod
    def technique_status(cls):
        """
        Gets the status of a certain attack technique.
        :return: ScanStatus numeric value
        """
        if mongo.db.telemetry.find_one({'telem_category': 'attack',
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
        return data

    @classmethod
    def get_base_data_by_status(cls, status):
        data = cls.get_message_and_status(status)
        data.update({'title': cls.technique_title()})
        return data


class UsageTechnique(AttackTechnique):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def parse_usages(usage):
        """
        Parses data from database and translates usage enums into strings
        :param usage: Usage telemetry that contains fields: {'usage': 'SMB', 'status': 1}
        :return: usage string
        """
        try:
            usage['usage'] = UsageEnum[usage['usage']].value[usage['status']]
        except KeyError:
            logger.error("Error translating usage enum. into string. "
                         "Check if usage enum field exists and covers all telem. statuses.")
        return usage

    @classmethod
    def get_usage_data(cls):
        data = list(mongo.db.telemetry.aggregate(cls.get_usage_query()))
        return list(map(cls.parse_usages, data))

    @classmethod
    def get_usage_query(cls):
        """
        :return: Query that parses attack telems for simple report component
        (gets machines and attack technique usage).
        """
        return [{'$match': {'telem_category': 'attack',
                            'data.technique': cls.tech_id}},
                {'$lookup': {'from': 'monkey',
                             'localField': 'monkey_guid',
                             'foreignField': 'guid',
                             'as': 'monkey'}},
                {'$project': {'monkey': {'$arrayElemAt': ['$monkey', 0]},
                              'status': '$data.status',
                              'usage': '$data.usage'}},
                {'$addFields': {'_id': 0,
                                'machine': {'hostname': '$monkey.hostname', 'ips': '$monkey.ip_addresses'},
                                'monkey': 0}},
                {'$group': {'_id': {'machine': '$machine', 'status': '$status', 'usage': '$usage'}}},
                {"$replaceRoot": {"newRoot": "$_id"}}]
