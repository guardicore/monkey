from infection_monkey.transport.attack_telems.base_telem import AttackTelem

__author__ = "VakarisZ"


class VictimHostTelem(AttackTelem):

    def __init__(self, technique, status, machine, data=None):
        """
        ATT&CK telemetry that parses and sends VictimHost telemetry
        :param technique: Technique ID. E.g. T111
        :param status: int from ScanStatus Enum
        :param machine: VictimHost obj from model/host.py
        :param data: Other data relevant to the attack technique
        """
        super(VictimHostTelem, self).__init__(technique, status, data, machine=False)
        victim_host = {'hostname': machine.domain_name, 'ip': machine.ip_addr}
        if data:
            self.data.update(data)
        if machine:
            self.data.update({'machine': victim_host})
