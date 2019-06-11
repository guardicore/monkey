from infection_monkey.transport.attack_telems.base_telem import AttackTelem

__author__ = "VakarisZ"


class VictimHostTelem(AttackTelem):

    def __init__(self, technique, status, machine, data=None):
        """
        ATT&CK telemetry that parses and sends VictimHost's (remote machine's) data
        :param technique: Technique ID. E.g. T111
        :param status: int from ScanStatus Enum
        :param machine: VictimHost obj from model/host.py
        :param data: Other data relevant to the attack technique
        """
        super(VictimHostTelem, self).__init__(technique, status, data)
        victim_host = {'domain_name': machine.domain_name, 'ip_addr': machine.ip_addr}
        self.data.update({'machine': victim_host})
