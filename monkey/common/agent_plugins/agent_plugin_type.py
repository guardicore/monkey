from enum import Enum


class AgentPluginType(Enum):
    CREDENTIALS_COLLECTOR = "Credentials_Collector"
    EXPLOITER = "Exploiter"
    FINGERPRINTER = "Fingerprinter"
    PAYLOAD = "Payload"
