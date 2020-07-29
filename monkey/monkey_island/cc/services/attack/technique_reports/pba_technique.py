import abc
from typing import List

from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class PostBreachTechnique(AttackTechnique, metaclass=abc.ABCMeta):
    """ Class for ATT&CK report components of post-breach actions """

    @property
    @abc.abstractmethod
    def pba_names(self) -> List[str]:
        """
        :return: names of post breach action
        """
        pass

    @classmethod
    def get_pba_query(cls, post_breach_action_names):
        """
        :param post_breach_action_names: Names of post-breach actions with which the technique is associated
        (example - `["Communicate as new user", "Backdoor user"]` for T1136)
        :return: Mongo query that parses attack telemetries for a simple report component
        (gets machines and post-breach action usage).
        """
        return [{'$match': {'telem_category': 'post_breach',
                            '$or': [{'data.name': pba_name} for pba_name in post_breach_action_names]}},
                {'$project': {'_id': 0,
                              'machine': {'hostname': '$data.hostname',
                                          'ips': ['$data.ip']},
                              'result': '$data.result'}}]

    @classmethod
    def get_report_data(cls):
        """
        :return: Technique's report data aggregated from the database
        """
        @cls.is_status_disabled
        def get_technique_status_and_data():
            info = list(mongo.db.telemetry.aggregate(cls.get_pba_query(cls.pba_names)))
            status = ScanStatus.UNSCANNED.value
            if info:
                successful_PBAs = mongo.db.telemetry.count({
                    '$or': [{'data.name': pba_name} for pba_name in cls.pba_names],
                    'data.result.1': True
                })
                status = ScanStatus.USED.value if successful_PBAs else ScanStatus.SCANNED.value
            return (status, info)

        data = {'title': cls.technique_title()}
        status, info = get_technique_status_and_data()

        data.update(cls.get_base_data_by_status(status))
        data.update({'info': info})
        return data
