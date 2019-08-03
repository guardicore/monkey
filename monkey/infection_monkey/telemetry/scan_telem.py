from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "itay.mizeretz"


class ScanTelem(BaseTelem):

    def __init__(self, machine):
        """
        Default scan telemetry constructor
        :param machine: Scanned machine
        """
        super(ScanTelem, self).__init__()
        self.machine = machine

    telem_category = 'scan'

    def get_data(self):
        return {
            'machine': self.machine.as_dict(),
            'service_count': len(self.machine.services)
        }
