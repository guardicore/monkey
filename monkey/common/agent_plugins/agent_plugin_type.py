from enum import Enum


class AgentPluginType(Enum):
    CREDENTIAL_COLLECTOR = "CredentialCollector"
    EXPLOITER = "Exploiter"
    FINGERPRINTER = "Fingerprinter"
    PAYLOAD = "Payload"
