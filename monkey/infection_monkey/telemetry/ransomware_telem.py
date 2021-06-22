from typing import List, Tuple

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem


class RansomwareTelem(BaseTelem):
    def __init__(self, attempts: List[Tuple[str, str]]):
        """
        Ransomware telemetry constructor
        :param attempts: List of tuples with each tuple containing the path
                         of a file it tried encrypting and its result.
                         If ransomware fails completely - list of one tuple
                         containing the directory path and error string.
        """
        super().__init__()
        self.attempts = attempts

    telem_category = TelemCategoryEnum.RANSOMWARE

    def get_data(self):
        return {"ransomware_attempts": self.attempts}
