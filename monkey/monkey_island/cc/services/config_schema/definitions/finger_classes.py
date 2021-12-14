FINGER_CLASSES = {
    "title": "Fingerprinters",
    "description": "Fingerprint modules collect info about external services "
    "Infection Monkey scans.",
    "type": "string",
    "anyOf": [
        {
            "type": "string",
            "enum": ["SMBFinger"],
            "title": "SMB Fingerprinter",
            "safe": True,
            "info": "Figures out if SMB is running and what's the version of it.",
            "attack_techniques": ["T1210"],
        },
        {
            "type": "string",
            "enum": ["SSHFinger"],
            "title": "SSH Fingerprinter",
            "safe": True,
            "info": "Figures out if SSH is running.",
            "attack_techniques": ["T1210"],
        },
        {
            "type": "string",
            "enum": ["HTTPFinger"],
            "title": "HTTP Fingerprinter",
            "safe": True,
            "info": "Checks if host has HTTP/HTTPS ports open.",
        },
        {
            "type": "string",
            "enum": ["MSSQLFinger"],
            "title": "MSSQL Fingerprinter",
            "safe": True,
            "info": "Checks if Microsoft SQL service is running and tries to gather "
            "information about it.",
            "attack_techniques": ["T1210"],
        },
        {
            "type": "string",
            "enum": ["ElasticFinger"],
            "title": "Elastic Fingerprinter",
            "safe": True,
            "info": "Checks if ElasticSearch is running and attempts to find it's " "version.",
            "attack_techniques": ["T1210"],
        },
    ],
}
