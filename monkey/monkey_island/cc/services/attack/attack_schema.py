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
                },
                "T1105": {
                    "title": "T1105 Remote file copy",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Files may be copied from one system to another to stage "
                                   "adversary tools or other files over the course of an operation."
                },
                "T1021": {
                    "title": "T1021 Remote services",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "depends_on": ["T1110"],
                    "description": "An adversary may use Valid Accounts to log into a service"
                                   " specifically designed to accept remote connections."
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
                    "value": True,
                    "necessary": False,
                    "description": "Adversaries may use brute force techniques to attempt access to accounts "
                                   "when passwords are unknown or when password hashes are obtained.",
                    "depends_on": ["T1210", "T1021"]
                },
                "T1003": {
                    "title": "T1003 Credential dumping",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "Mapped with T1078 Valid Accounts because both techniques require"
                                   " same credential harvesting modules. "
                                   "Credential dumping is the process of obtaining account login and password "
                                   "information, normally in the form of a hash or a clear text password, "
                                   "from the operating system and software.",
                    "depends_on": ["T1078"]
                },
                "T1145": {
                    "title": "T1145 Private keys",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "Adversaries may gather private keys from compromised systems for use in "
                                   "authenticating to Remote Services like SSH or for use in decrypting "
                                   "other collected files such as email.",
                    "depends_on": ["T1110", "T1210"]
                }
            }
        },
        "defence_evasion": {
            "title": "Defence evasion",
            "type": "object",
            "properties": {
                "T1197": {
                    "title": "T1197 BITS jobs",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may abuse BITS to download, execute, "
                                   "and even clean up after running malicious code."
                },
                "T1107": {
                    "title": "T1107 File Deletion",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may remove files over the course of an intrusion "
                                   "to keep their footprint low or remove them at the end as part "
                                   "of the post-intrusion cleanup process."
                },
                "T1222": {
                    "title": "T1222 File permissions modification",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may modify file permissions/attributes to evade intended DACLs."
                }
            }
        },
        "execution": {
            "title": "Execution",
            "type": "object",
            "properties": {
                "T1035": {
                    "title": "T1035 Service execution",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "Adversaries may execute a binary, command, or script via a method "
                                   "that interacts with Windows services, such as the Service Control Manager.",
                    "depends_on": ["T1210"]
                },
                "T1129": {
                    "title": "T1129 Execution through module load",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "The Windows module loader can be instructed to load DLLs from arbitrary "
                                   "local paths and arbitrary Universal Naming Convention (UNC) network paths.",
                    "depends_on": ["T1078", "T1003"]
                },
                "T1106": {
                    "title": "T1106 Execution through API",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "description": "Adversary tools may directly use the Windows application "
                                   "programming interface (API) to execute binaries.",
                    "depends_on": ["T1210"]
                },
                "T1059": {
                    "title": "T1059 Command line interface",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may use command-line interfaces to interact with systems "
                                   "and execute other software during the course of an operation.",
                },
                "T1086": {
                    "title": "T1086 Powershell",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries can use PowerShell to perform a number of exploiters,"
                                   " including discovery of information and execution of code.",
                },
                "T1064": {
                    "title": "T1064 Scripting",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may use scripts to aid in operations and "
                                   "perform multiple exploiters that would otherwise be manual.",
                }
            }
        },
        "discovery": {
            "title": "Discovery",
            "type": "object",
            "properties": {
                "T1082": {
                    "title": "T1082 System information discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "depends_on": ["T1016", "T1005"],
                    "description": "An adversary may attempt to get detailed information about the "
                                   "operating system and hardware, including version, patches, hotfixes, "
                                   "service packs, and architecture."
                },
                "T1018": {
                    "title": "T1018 Remote System Discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries will likely attempt to get a listing of other systems by IP address, "
                                   "hostname, or other logical identifier on a network for lateral movement."
                },
                "T1016": {
                    "title": "T1016 System network configuration discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "depends_on": ["T1005", "T1082"],
                    "description": "Adversaries will likely look for details about the network configuration "
                                   "and settings of systems they access or through information discovery"
                                   " of remote systems."
                }
            }
        },
        "collection": {
            "title": "Collection",
            "type": "object",
            "properties": {
                "T1005": {
                    "title": "T1005 Data from local system",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "depends_on": ["T1016", "T1082"],
                    "description": "Sensitive data can be collected from local system sources, such as the file system "
                                   "or databases of information residing on the system prior to Exfiltration."
                }
            }
        },
        "command_and_control": {
            "title": "Command and Control",
            "type": "object",
            "properties": {
                "T1065": {
                    "title": "T1065 Uncommonly used port",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Adversaries may conduct C2 communications over a non-standard "
                                   "port to bypass proxies and firewalls that have been improperly configured."
                },
                "T1090": {
                    "title": "T1090 Connection proxy",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "A connection proxy is used to direct network traffic between systems "
                                   "or act as an intermediary for network communications."
                },
                "T1188": {
                    "title": "T1188 Multi-hop proxy",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "To disguise the source of malicious traffic, "
                                   "adversaries may chain together multiple proxies."
                }
            }
        },
        "exfiltration": {
            "title": "Exfiltration",
            "type": "object",
            "properties": {
                "T1041": {
                    "title": "T1041 Exfiltration Over Command and Control Channel",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "description": "Data exfiltration is performed over the Command and Control channel."
                }
            }
        }
    }
}
