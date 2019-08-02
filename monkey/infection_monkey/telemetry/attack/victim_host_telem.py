from infection_monkey.telemetry.attack.attack_telem import AttackTelem

__author__ = "VakarisZ"


class VictimHostTelem(AttackTelem):

    def __init__(self, technique, status, machine):
        """
        ATT&CK telemetry.
        When `send` is called, it will parse and send the VictimHost's (remote machine's) data.
        :param technique: Technique ID. E.g. T111
        :param status: ScanStatus of technique
        :param machine: VictimHost obj from model/host.py
        """
        super(VictimHostTelem, self).__init__(technique, status)
        self.machine = {'domain_name': machine.domain_name, 'ip_addr': machine.ip_addr}

    def get_data(self):
        data = super(VictimHostTelem, self).get_data()
        data.update({
            'machine': self.machine
        })
        return data
