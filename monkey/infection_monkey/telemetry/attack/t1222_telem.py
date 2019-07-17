from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class T1222Telem(AttackTelem):
    def __init__(self, status, command):
        """
        T1222 telemetry.
        :param status: ScanStatus of technique
        :param command: command used to change permissions
        """
        super(T1222Telem, self).__init__('T1222', status)
        self.command = command

    def get_data(self):
        data = super(T1222Telem, self).get_data()
        data.update({
            'command': self.command
        })
        return data
