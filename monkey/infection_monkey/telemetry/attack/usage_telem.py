from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class UsageTelem(AttackTelem):

    def __init__(self, technique, status, usage):
        """
        :param technique: Id of technique
        :param status: ScanStatus of technique
        :param usage: Enum of UsageEnum type
        """
        super(UsageTelem, self).__init__(technique, status)
        self.usage = usage.name

    def get_data(self):
        data = super(UsageTelem, self).get_data()
        data.update({
            'usage': self.usage
        })
        return data
