from common.common_consts.credential_collector_names import MIMIKATZ_COLLECTOR, SSH_COLLECTOR

CREDENTIAL_COLLECTOR_CLASSES = {
    "title": "Credential Collectors",
    "description": "Click on a credential collector to find out what it collects.",
    "type": "string",
    "anyOf": [
        {
            "type": "string",
            "enum": [MIMIKATZ_COLLECTOR],
            "title": "Mimikatz Credentials Collector",
            "safe": True,
            "info": "Collects credentials from Windows credential manager.",
            "attack_techniques": ["T1003", "T1005"],
        },
        {
            "type": "string",
            "enum": [SSH_COLLECTOR],
            "title": "SSH Credentials Collector",
            "safe": True,
            "info": "Searches users' home directories and collects SSH keypairs.",
            "attack_techniques": ["T1005", "T1145"],
        },
    ],
}
