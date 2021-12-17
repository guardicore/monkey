import threading
from typing import Dict

from infection_monkey.payload.i_payload import IPayload

from . import ransomware_builder


class RansomwarePayload(IPayload):
    def run(self, options: Dict, interrupt: threading.Event):
        ransomware = ransomware_builder.build_ransomware(options)
        ransomware.run(interrupt)
