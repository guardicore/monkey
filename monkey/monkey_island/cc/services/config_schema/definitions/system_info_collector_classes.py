from common.common_consts.system_info_collectors_names import (
    MIMIKATZ_COLLECTOR,
    PROCESS_LIST_COLLECTOR,
    SSH_COLLECTOR,
)

SYSTEM_INFO_COLLECTOR_CLASSES = {
    "title": "System Information Collectors",
    "description": "Click on a system info collector to find out what it collects.",
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
            "enum": [PROCESS_LIST_COLLECTOR],
            "title": "Process List Collector",
            "safe": True,
            "info": "Collects a list of running processes on the machine.",
            "attack_techniques": ["T1082"],
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
