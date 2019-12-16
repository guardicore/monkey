from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class T1005Telem(AttackTelem):
    def __init__(self, status, gathered_data_type, info=""):
        """
        T1005 telemetry.
        :param status: ScanStatus of technique
        :param gathered_data_type: Type of data collected from local system
        :param info: Additional info about data
        """
        super(T1005Telem, self).__init__('T1005', status)
        self.gathered_data_type = gathered_data_type
        self.info = info

    def get_data(self):
        data = super(T1005Telem, self).get_data()
        data.update({
            'gathered_data_type': self.gathered_data_type,
            'info': self.info
        })
        return data
