from infection_monkey.telemetry.attack.usage_telem import UsageTelem


class T1129Telem(UsageTelem):
    def __init__(self, status, usage):
        """
        T1129 telemetry.
        :param status: ScanStatus of technique
        :param usage: Enum of UsageEnum type
        """
        super(T1129Telem, self).__init__("T1129", status, usage)
