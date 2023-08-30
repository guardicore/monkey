from enum import StrEnum


class AgentPluginType(StrEnum):
    CREDENTIALS_COLLECTOR = "Credentials_Collector"
    EXPLOITER = "Exploiter"
    FINGERPRINTER = "Fingerprinter"
    PAYLOAD = "Payload"
