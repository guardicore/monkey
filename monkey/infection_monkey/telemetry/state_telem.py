from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "itay.mizeretz"


class StateTelem(BaseTelem):

    def __init__(self, is_done, version="Unknown"):
        """
        Default state telemetry constructor
        :param is_done: Whether the state of monkey is done.
        """
        super(StateTelem, self).__init__()
        self.is_done = is_done
        self.version = version

    telem_category = 'state'

    def get_data(self):
        return {
            'done': self.is_done,
            'version': self.version
        }
