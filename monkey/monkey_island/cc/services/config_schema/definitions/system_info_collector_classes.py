from common.common_consts.system_info_collectors_names import (
    MIMIKATZ_COLLECTOR,
)

SYSTEM_INFO_COLLECTOR_CLASSES = {
    "title": "System Information Collectors",
    "description": "Click on a system info collector to find out what it collects.",
    "type": "string",
    "anyOf": [
        {
            "type": "string",
            "enum": [MIMIKATZ_COLLECTOR],
            "title": "Mimikatz Collector",
            "safe": True,
            "info": "Collects credentials from Windows credential manager.",
            "attack_techniques": ["T1003", "T1005"],
        },
    ],
}
