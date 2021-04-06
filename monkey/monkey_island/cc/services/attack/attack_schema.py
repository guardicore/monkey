SCHEMA = {
    "title": "ATT&CK configuration",
    "type": "object",
    "properties": {
        "execution": {
            "title": "Execution",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0002/",
            "properties": {
                "T1059": {
                    "title": "Command line interface",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1059",
                    "description": "Adversaries may use command-line interfaces to interact with systems "
                                   "and execute other software during the course of an operation.",
                },
                "T1129": {
                    "title": "Execution through module load",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1129",
                    "description": "The Windows module loader can be instructed to load DLLs from arbitrary "
                                   "local paths and arbitrary Universal Naming Convention (UNC) network paths.",
                    "depends_on": ["T1078", "T1003"]
                },
                "T1106": {
                    "title": "Execution through API",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1106",
                    "description": "Adversary tools may directly use the Windows application "
                                   "programming interface (API) to execute binaries.",
                    "depends_on": ["T1210"]
                },
                "T1086": {
                    "title": "Powershell",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1086",
                    "description": "Adversaries can use PowerShell to perform a number of actions,"
                                   " including discovery of information and execution of code.",
                },
                "T1064": {
                    "title": "Scripting",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1064",
                    "description": "Adversaries may use scripts to aid in operations and "
                                   "perform multiple actions that would otherwise be manual.",
                },
                "T1035": {
                    "title": "Service execution",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1035",
                    "description": "Adversaries may execute a binary, command, or script via a method "
                                   "that interacts with Windows services, such as the Service Control Manager.",
                    "depends_on": ["T1210"]
                },
                "T1154": {
                    "title": "Trap",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1154",
                    "description": "Adversaries can use the trap command to register code to be executed "
                                   "when the shell encounters specific interrupts."
                }
            },
        },
        "persistence": {
            "title": "Persistence",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0003/",
            "properties": {
                "T1156": {
                    "title": ".bash_profile and .bashrc",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1156",
                    "description": "Adversaries may abuse shell scripts by "
                                   "inserting arbitrary shell commands to gain persistence, which "
                                   "would be executed every time the user logs in or opens a new shell.",
                    "depends_on": ["T1504"]
                },
                "T1136": {
                    "title": "Create account",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1136",
                    "description": "Adversaries with a sufficient level of access "
                                   "may create a local system, domain, or cloud tenant account."
                },
                "T1158": {
                    "title": "Hidden files and directories",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1158",
                    "description": "Adversaries can hide files and folders on the system "
                                   "and evade a typical user or system analysis that does not "
                                   "incorporate investigation of hidden files."
                },
                "T1168": {
                    "title": "Local job scheduling",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1168/",
                    "description": "Linux supports multiple methods for creating pre-scheduled and "
                                   "periodic background jobs. Job scheduling can be used by adversaries to "
                                   "schedule running malicious code at some specified date and time.",
                    "depends_on": ["T1053"]
                },
                "T1504": {
                    "title": "PowerShell profile",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1504",
                    "description": "Adversaries may gain persistence and elevate privileges "
                                   "in certain situations by abusing PowerShell profiles which "
                                   "are scripts that run when PowerShell starts.",
                    "depends_on": ["T1156"]
                },
                "T1053": {
                    "title": "Scheduled task",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1053",
                    "description": "Windows utilities can be used to schedule programs or scripts to "
                                   "be executed at a date and time. An adversary may use task scheduling to "
                                   "execute programs at system startup or on a scheduled basis for persistence.",
                    "depends_on": ["T1168"]
                },
                "T1166": {
                    "title": "Setuid and Setgid",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1166",
                    "description": "Adversaries can set the setuid or setgid bits to get code running in "
                                   "a different user’s context."
                }
            }
        },
        "defence_evasion": {
            "title": "Defence evasion",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0005/",
            "properties": {
                "T1197": {
                    "title": "BITS jobs",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1197",
                    "description": "Adversaries may abuse BITS to download, execute, "
                                   "and even clean up after running malicious code."
                },
                "T1146": {
                    "title": "Clear command history",
                    "type": "bool",
                    "value": False,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1146",
                    "description": "Adversaries may clear/disable command history of a compromised "
                                   "account to conceal the actions undertaken during an intrusion."
                },
                "T1107": {
                    "title": "File Deletion",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1107",
                    "description": "Adversaries may remove files over the course of an intrusion "
                                   "to keep their footprint low or remove them at the end as part "
                                   "of the post-intrusion cleanup process."
                },
                "T1222": {
                    "title": "File permissions modification",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1222",
                    "description": "Adversaries may modify file permissions/attributes to evade intended DACLs."
                },
                "T1099": {
                    "title": "Timestomping",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1099",
                    "description": "Adversaries may modify file time attributes to hide new/changes to existing "
                                   "files to avoid attention from forensic investigators or file analysis tools."
                },
                "T1216": {
                    "title": "Signed script proxy execution",
                    "type": "bool",
                    "value": False,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1216",
                    "description": "Adversaries may use scripts signed with trusted certificates to "
                                   "proxy execution of malicious files on Windows systems."
                }
            }
        },
        "credential_access": {
            "title": "Credential access",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0006/",
            "properties": {
                "T1110": {
                    "title": "Brute force",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1110",
                    "description": "Adversaries may use brute force techniques to attempt access to accounts "
                                   "when passwords are unknown or when password hashes are obtained.",
                    "depends_on": ["T1210", "T1021"]
                },
                "T1003": {
                    "title": "Credential dumping",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1003",
                    "description": "Mapped with T1078 Valid Accounts because both techniques require"
                                   " same credential harvesting modules. "
                                   "Credential dumping is the process of obtaining account login and password "
                                   "information, normally in the form of a hash or a clear text password, "
                                   "from the operating system and software.",
                    "depends_on": ["T1078"]
                },
                "T1145": {
                    "title": "Private keys",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1145",
                    "description": "Adversaries may gather private keys from compromised systems for use in "
                                   "authenticating to Remote Services like SSH or for use in decrypting "
                                   "other collected files such as email.",
                    "depends_on": ["T1110", "T1210"]
                }
            }
        },
        "discovery": {
            "title": "Discovery",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0007/",
            "properties": {
                "T1087": {
                    "title": "Account Discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1087",
                    "description": "Adversaries may attempt to get a listing of accounts on a system or "
                                   "within an environment. This information can help adversaries determine which "
                                   "accounts exist to aid in follow-on behavior."
                },
                "T1018": {
                    "title": "Remote System Discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1018",
                    "description": "Adversaries will likely attempt to get a listing of other systems by IP address, "
                                   "hostname, or other logical identifier on a network for lateral movement."
                },
                "T1082": {
                    "title": "System information discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1082",
                    "depends_on": ["T1016", "T1005"],
                    "description": "An adversary may attempt to get detailed information about the "
                                   "operating system and hardware, including version, patches, hotfixes, "
                                   "service packs, and architecture."
                },
                "T1016": {
                    "title": "System network configuration discovery",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1016",
                    "depends_on": ["T1005", "T1082"],
                    "description": "Adversaries will likely look for details about the network configuration "
                                   "and settings of systems they access or through information discovery"
                                   " of remote systems."
                }
            }
        },
        "lateral_movement": {
            "title": "Lateral movement",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0008/",
            "properties": {
                "T1210": {
                    "title": "Exploitation of Remote services",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1210",
                    "description": "Exploitation of a software vulnerability occurs when an adversary "
                                   "takes advantage of a programming error in a program, service, or within the "
                                   "operating system software or kernel itself to execute adversary-controlled code."
                },
                "T1075": {
                    "title": "Pass the hash",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1075",
                    "description": "Pass the hash (PtH) is a method of authenticating as a user without "
                                   "having access to the user's cleartext password."
                },
                "T1105": {
                    "title": "Remote file copy",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1105",
                    "description": "Files may be copied from one system to another to stage "
                                   "adversary tools or other files over the course of an operation."
                },
                "T1021": {
                    "title": "Remote services",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1021",
                    "depends_on": ["T1110"],
                    "description": "An adversary may use Valid Accounts to log into a service"
                                   " specifically designed to accept remote connections."
                }
            }
        },
        "collection": {
            "title": "Collection",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0009/",
            "properties": {
                "T1005": {
                    "title": "Data from local system",
                    "type": "bool",
                    "value": True,
                    "necessary": False,
                    "link": "https://attack.mitre.org/techniques/T1005",
                    "depends_on": ["T1016", "T1082"],
                    "description": "Sensitive data can be collected from local system sources, such as the file system "
                                   "or databases of information residing on the system prior to Exfiltration."
                }
            }
        },
        "command_and_control": {
            "title": "Command and Control",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0011/",
            "properties": {
                "T1090": {
                    "title": "Connection proxy",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1090",
                    "description": "A connection proxy is used to direct network traffic between systems "
                                   "or act as an intermediary for network communications."
                },
                "T1065": {
                    "title": "Uncommonly used port",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1065",
                    "description": "Adversaries may conduct C2 communications over a non-standard "
                                   "port to bypass proxies and firewalls that have been improperly configured."
                },
                "T1188": {
                    "title": "Multi-hop proxy",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1188",
                    "description": "To disguise the source of malicious traffic, "
                                   "adversaries may chain together multiple proxies."
                }
            }
        },
        "exfiltration": {
            "title": "Exfiltration",
            "type": "object",
            "link": "https://attack.mitre.org/tactics/TA0010/",
            "properties": {
                "T1041": {
                    "title": "Exfiltration Over Command and Control Channel",
                    "type": "bool",
                    "value": True,
                    "necessary": True,
                    "link": "https://attack.mitre.org/techniques/T1041",
                    "description": "Data exfiltration is performed over the Command and Control channel."
                }
            }
        }
    }
}
