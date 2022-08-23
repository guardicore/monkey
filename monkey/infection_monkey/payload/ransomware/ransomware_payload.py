import threading
from typing import Dict

from infection_monkey.payload.i_payload import IPayload
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

from . import ransomware_builder


class RansomwarePayload(IPayload):
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        self._telemetry_messenger = telemetry_messenger

    def run(self, options: Dict, interrupt: threading.Event):
        ransomware = ransomware_builder.build_ransomware(options, self._telemetry_messenger)
        ransomware.run(interrupt)
