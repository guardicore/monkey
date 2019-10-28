from infection_monkey.telemetry.attack.usage_telem import UsageTelem


class T1035Telem(UsageTelem):
    def __init__(self, status, usage):
        """
        T1035 telemetry.
        :param status: ScanStatus of technique
        :param usage: Enum of UsageEnum type
        """
        super(T1035Telem, self).__init__('T1035', status, usage)
