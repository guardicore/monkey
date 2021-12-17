from enum import Enum


class PluginType(Enum):
    EXPLOITER = "Exploiter"
    FINGERPRINTER = "Fingerprinter"
    PAYLOAD = "Payload"
    POST_BREACH_ACTION = "PBA"
    SYSTEM_INFO_COLLECTOR = "SystemInfoCollector"
