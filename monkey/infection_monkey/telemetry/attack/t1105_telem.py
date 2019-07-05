from infection_monkey.telemetry.attack.victim_host_telem import AttackTelem


class T1105Telem(AttackTelem):
    def __init__(self, status, host, path):
        """
        T1105 telemetry.
        :param status: ScanStatus of technique
        :param host: IP of machine which downloaded the file
        :param path: Uploaded file's path
        """
        super(T1105Telem, self).__init__('T1105', status)
        self.path = path
        self.host = host

    def get_data(self):
        data = super(T1105Telem, self).get_data()
        data.update({
            'path': self.path,
            'host': self.host
        })
        return data
