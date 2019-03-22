SCHEMA = {
    "title": "ATT&CK configuration",
    "type": "object",
    "properties": {
        "lateral_movement": {
            "title": "Lateral movement",
            "type": "object",
            "properties": {
                "T1210": {
                    "title": "T1210 Exploitation of Remote services",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "Exploitation of a software vulnerability occurs when an adversary "
                                   "takes advantage of a programming error in a program, service, or within the "
                                   "operating system software or kernel itself to execute adversary-controlled code."
                },
                "T1075": {
                    "title": "T1075 Pass the hash",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "Pass the hash (PtH) is a method of authenticating as a user without "
                                   "having access to the user's cleartext password."
                }
            }
        },
        "credential_access": {
            "title": "Credential access",
            "type": "object",
            "properties": {
                "T1110": {
                    "title": "T1110 Brute force",
                    "type": "bool",
                    "value": False,
                    "necessary": False,
                    "description": "Adversaries may use brute force techniques to attempt access to accounts "
                                   "when passwords are unknown or when password hashes are obtained."
                }
            }
        },
        "defence_evasion": {
            "title": "Defence evasion",
            "type": "object",
            "properties": {
                "T1197": {
                    "title": "T1197 Bits jobs",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may abuse BITS to download, execute, "
                                   "and even clean up after running malicious code."
                }
            }
        },
    }
}
