from pathlib import Path
from typing import Union

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.victim_host_telem import AttackTelem


class T1105Telem(AttackTelem):
    def __init__(self, status: ScanStatus, src: str, dst: str, filename: Union[Path, str]):
        """
        T1105 telemetry.
        :param status: ScanStatus of technique
        :param src: IP of machine which uploaded the file
        :param dst: IP of machine which downloaded the file
        :param filename: Uploaded file's name
        """
        super(T1105Telem, self).__init__("T1105", status)
        self.filename = str(filename)
        self.src = src
        self.dst = dst

    def get_data(self):
        data = super(T1105Telem, self).get_data()
        data.update({"filename": self.filename, "src": self.src, "dst": self.dst})
        return data
