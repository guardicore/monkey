from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class T1035Telem(AttackTelem):
    def __init__(self, status, usage):
        """
        T1035 telemetry.
        :param status: ScanStatus of technique
        :param usage: Usage string
        """
        super(T1035Telem, self).__init__('T1035', status)
        self.usage = usage

    def get_data(self):
        data = super(T1035Telem, self).get_data()
        data.update({
            'usage': self.usage
        })
        return data
