import abc

from monkey_island.cc.services.attack.attack_config import AttackConfig
from monkey_island.cc.database import mongo
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class PostBreachTechnique(AttackTechnique, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def pba_names(self):
        """
        :return: name of post breach action
        """
        pass

    @classmethod
    def get_pba_query(cls, post_breach_action_names):
        return [{'$match': {'telem_category': 'post_breach',
                            # 'data.name': post_breach_action_name}},
                            '$or': [{'data.name': pba_name} for pba_name in post_breach_action_names]}},
                {'$project': {'_id': 0,
                              'machine': {'hostname': '$data.hostname',
                                          'ips': ['$data.ip']},
                              'result': '$data.result'}}]

    @classmethod
    def get_report_data(cls):
        data = {'title': cls.technique_title(), 'info': []}

        info = list(mongo.db.telemetry.aggregate(cls.get_pba_query(cls.pba_names)))

        status = []
        for pba_node in info:
            status.append(pba_node['result'][1])
        status = (ScanStatus.USED.value if any(status) else ScanStatus.SCANNED.value)\
            if status else ScanStatus.UNSCANNED.value

        if status == ScanStatus.UNSCANNED.value and\
           not AttackConfig.get_technique_values()[cls.tech_id]:
            status = ScanStatus.DISABLED.value

        data.update(cls.get_base_data_by_status(status))
        data.update({'info': info})
        return data
