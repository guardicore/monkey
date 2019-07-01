from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class UsageTelem(AttackTelem):

    def __init__(self, technique, status, usage):
        """
        T1035 telemetry.
        :param status: ScanStatus of technique
        :param usage: Usage string
        """
        super(UsageTelem, self).__init__(technique, status)
        self.usage = usage

    def get_data(self):
        data = super(UsageTelem, self).get_data()
        data.update({
            'usage': self.usage
        })
        return data
