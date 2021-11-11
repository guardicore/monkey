from common.common_consts.system_info_collectors_names import (
    AWS_COLLECTOR,
    AZURE_CRED_COLLECTOR,
    ENVIRONMENT_COLLECTOR,
    HOSTNAME_COLLECTOR,
    MIMIKATZ_COLLECTOR,
)

SYSTEM_INFO_COLLECTOR_CLASSES = {
    "title": "System Information Collectors",
    "description": "Click on a system info collector to find out what it collects.",
    "type": "string",
    "anyOf": [
        {
            "type": "string",
            "enum": [ENVIRONMENT_COLLECTOR],
            "title": "Environment Collector",
            "safe": True,
            "info": "Collects information about machine's environment (on " "premise/GCP/AWS).",
            "attack_techniques": ["T1082"],
        },
        {
            "type": "string",
            "enum": [MIMIKATZ_COLLECTOR],
            "title": "Mimikatz Collector",
            "safe": True,
            "info": "Collects credentials from Windows credential manager.",
            "attack_techniques": ["T1003", "T1005"],
        },
        {
            "type": "string",
            "enum": [AWS_COLLECTOR],
            "title": "AWS Collector",
            "safe": True,
            "info": "If on AWS, collects more information about the AWS instance "
            "currently running on.",
            "attack_techniques": ["T1082"],
        },
        {
            "type": "string",
            "enum": [HOSTNAME_COLLECTOR],
            "title": "Hostname Collector",
            "safe": True,
            "info": "Collects machine's hostname.",
            "attack_techniques": ["T1082", "T1016"],
        },
        {
            "type": "string",
            "enum": [AZURE_CRED_COLLECTOR],
            "title": "Azure Credential Collector",
            "safe": True,
            "info": "Collects password credentials from Azure VMs",
            "attack_techniques": ["T1003", "T1005"],
        },
    ],
}
