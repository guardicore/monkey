import abc

from common.utils.attack_utils import UsageEnum
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import (
    AttackTechnique, logger)


class UsageTechnique(AttackTechnique, metaclass=abc.ABCMeta):
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
        """
        Gets data of usage attack telemetries
        :return: parsed list of usages from attack telemetries of usage type
        """
        data = list(mongo.db.telemetry.aggregate(cls.get_usage_query()))
        return list(map(cls.parse_usages, data))

    @classmethod
    def get_usage_query(cls):
        """
        :return: Query that parses attack telemetries for a simple report component
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
