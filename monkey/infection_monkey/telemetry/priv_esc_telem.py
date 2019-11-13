from typing import List

from infection_monkey.telemetry.base_telem import BaseTelem


class PrivEscTelem(BaseTelem):

    def __init__(self, exploiter: "HostPrivExploiter", result: bool, info: List[object]=None):
        self.exploiter = exploiter
        self.result = result
        self.info = info
        super().__init__()

    telem_category = 'privilege_escalation'

    def get_data(self):
        return {
            'exploiter': self.exploiter,
            'result': self.result,
            'info': self.info
        }
