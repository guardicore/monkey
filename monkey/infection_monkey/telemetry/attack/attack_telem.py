from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "VakarisZ"


class AttackTelem(BaseTelem):

    def __init__(self, technique, status):
        """
        Default ATT&CK telemetry constructor
        :param technique: Technique ID. E.g. T111
        :param status: ScanStatus of technique
        """
        super(AttackTelem, self).__init__()
        self.technique = technique
        self.status = status

    telem_category = 'attack'

    def get_data(self):
        return {
            'status': self.status.value,
            'technique': self.technique
        }
