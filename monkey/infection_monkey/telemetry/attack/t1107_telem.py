from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class T1107Telem(AttackTelem):
    def __init__(self, status, path):
        """
        T1107 telemetry.
        :param status: ScanStatus of technique
        :param path: Path of deleted dir/file
        """
        super(T1107Telem, self).__init__('T1107', status)
        self.path = path

    def get_data(self):
        data = super(T1107Telem, self).get_data()
        data.update({
            'path': self.path
        })
        return data
