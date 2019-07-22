from infection_monkey.telemetry.attack.usage_telem import UsageTelem


class T1064Telem(UsageTelem):
    def __init__(self, status, usage):
        """
        T1064 telemetry.
        :param status: ScanStatus of technique
        :param usage: Usage string
        """
        super(T1064Telem, self).__init__('T1064', status, usage)
