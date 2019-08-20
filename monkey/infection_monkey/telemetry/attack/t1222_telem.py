from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem


class T1222Telem(VictimHostTelem):
    def __init__(self, status, command, machine):
        """
        T1222 telemetry.
        :param status: ScanStatus of technique
        :param command: command used to change permissions
        :param machine: VictimHost type object
        """
        super(T1222Telem, self).__init__('T1222', status, machine)
        self.command = command

    def get_data(self):
        data = super(T1222Telem, self).get_data()
        data.update({
            'command': self.command
        })
        return data
