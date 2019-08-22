from infection_monkey.telemetry.attack.usage_telem import AttackTelem


class T1064Telem(AttackTelem):
    def __init__(self, status, usage):
        """
        T1064 telemetry.
        :param status: ScanStatus of technique
        :param usage: Usage string
        """
        super(T1064Telem, self).__init__('T1064', status)
        self.usage = usage

    def get_data(self):
        data = super(T1064Telem, self).get_data()
        data.update({
            'usage': self.usage
        })
        return data
