from infection_monkey.telemetry.attack.usage_telem import UsageTelem


class T1106Telem(UsageTelem):
    def __init__(self, status, usage):
        """
        T1106 telemetry.
        :param status: ScanStatus of technique
        :param usage: Enum name of UsageEnum
        """
        super(T1106Telem, self).__init__("T1106", status, usage)
