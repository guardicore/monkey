from infection_monkey.telemetry.attack.attack_telem import AttackTelem


class T1145Telem(AttackTelem):
    def __init__(self, status, name, home_dir):
        """
        T1145 telemetry.
        :param status: ScanStatus of technique
        :param name: Username from which ssh keypair is taken
        :param home_dir: Home directory where we found the ssh keypair
        """
        super(T1145Telem, self).__init__("T1145", status)
        self.name = name
        self.home_dir = home_dir

    def get_data(self):
        data = super(T1145Telem, self).get_data()
        data.update({"name": self.name, "home_dir": self.home_dir})
        return data
