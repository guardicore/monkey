WARNING_SIGN = u" \u26A0"

SCHEMA = {
    "title": "Monkey",
    "type": "object",
    "definitions": {
        "exploiter_classes": {
            "title": "Exploit class",
            "type": "string",
            "anyOf": [
                {
                    "type": "string",
                    "enum": [
                        "SmbExploiter"
                    ],
                    "title": "SMB Exploiter",
                    "attack_techniques": ["T1110", "T1075"]
                },
                {
                    "type": "string",
                    "enum": [
                        "WmiExploiter"
                    ],
                    "title": "WMI Exploiter",
                    "attack_techniques": ["T1110"]
                },
                {
                    "type": "string",
                    "enum": [
                        "MSSQLExploiter"
                    ],
                    "title": "MSSQL Exploiter",
                    "attack_techniques": ["T1110"]
                },
                {
                    "type": "string",
                    "enum": [
                        "RdpExploiter"
                    ],
                    "title": "RDP Exploiter (UNSAFE)",
                    "attack_techniques": []
                },
                {
                    "type": "string",
                    "enum": [
                        "Ms08_067_Exploiter"
                    ],
                    "title": "MS08-067 Exploiter (UNSAFE)",
                    "attack_techniques": []
                },
                {
                    "type": "string",
                    "enum": [
                        "SSHExploiter"
                    ],
                    "title": "SSH Exploiter",
                    "attack_techniques": ["T1110", "T1145"]
                },
                {
                    "type": "string",
                    "enum": [
                        "ShellShockExploiter"
                    ],
                    "title": "ShellShock Exploiter"
                },
                {
                    "type": "string",
                    "enum": [
                        "SambaCryExploiter"
                    ],
                    "title": "SambaCry Exploiter"
                },
                {
                    "type": "string",
                    "enum": [
                        "ElasticGroovyExploiter"
                    ],
                    "title": "ElasticGroovy Exploiter"
                },
                {
                    "type": "string",
                    "enum": [
                        "Struts2Exploiter"
                    ],
                    "title": "Struts2 Exploiter"
                },
                {
                    "type": "string",
                    "enum": [
                        "WebLogicExploiter"
                    ],
                    "title": "WebLogic Exploiter"
                },
                {
                    "type": "string",
                    "enum": [
                        "HadoopExploiter"
                    ],
                    "title": "Hadoop/Yarn Exploiter"
                },
                {
                    "type": "string",
                    "enum": [
                        "VSFTPDExploiter"
                    ],
                    "title": "VSFTPD Exploiter"
                }
            ]
        },
        "post_breach_acts": {
            "title": "Post breach actions",
            "type": "string",
            "anyOf": [
                {
                    "type": "string",
                    "enum": [
                        "BackdoorUser"
                    ],
                    "title": "Back door user",
                    "attack_techniques": []
                },
            ],
        },
        "finger_classes": {
            "title": "Fingerprint class",
            "type": "string",
            "anyOf": [
                {
                    "type": "string",
                    "enum": [
                        "SMBFinger"
                    ],
                    "title": "SMBFinger",
                    "attack_techniques": ["T1210"]
                },
                {
                    "type": "string",
                    "enum": [
                        "SSHFinger"
                    ],
                    "title": "SSHFinger",
                    "attack_techniques": ["T1210"]
                },
                {
                    "type": "string",
                    "enum": [
                        "PingScanner"
                    ],
                    "title": "PingScanner"
                },
                {
                    "type": "string",
                    "enum": [
                        "HTTPFinger"
                    ],
                    "title": "HTTPFinger"
                },
                {
                    "type": "string",
                    "enum": [
                        "MySQLFinger"
                    ],
                    "title": "MySQLFinger",
                    "attack_techniques": ["T1210"]
                },
                {
                    "type": "string",
                    "enum": [
                        "MSSQLFinger"
                    ],
                    "title": "MSSQLFinger",
                    "attack_techniques": ["T1210"]
                },

                {
                    "type": "string",
                    "enum": [
                        "ElasticFinger"
                    ],
                    "title": "ElasticFinger",
                    "attack_techniques": ["T1210"]
                }
            ]
        }
    },
    "properties": {
        "basic": {
            "title": "Basic - Exploits",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "should_exploit": {
                            "title": "Exploit network machines",
                            "type": "boolean",
                            "default": True,
                            "attack_techniques": ["T1210"],
                            "description": "Determines if monkey should try to safely exploit machines on the network"
                        }
                    }
                },
                "credentials": {
                    "title": "Credentials",
                    "type": "object",
                    "properties": {
                        "exploit_user_list": {
                            "title": "Exploit user list",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                                "Administrator",
                                "root",
                                "user"
                            ],
                            "description": "List of usernames to use on exploits using credentials"
                        },
                        "exploit_password_list": {
                            "title": "Exploit password list",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                                "Password1!",
                                "1234",
                                "password",
                                "12345678"
                            ],
                            "description": "List of password to use on exploits using credentials"
                        }
                    }
                }
            }
        },
        "basic_network": {
            "title": "Basic - Network",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "blocked_ips": {
                            "title": "Blocked IPs",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                            ],
                            "description": "List of IPs to not scan"
                        },
                        "local_network_scan": {
                            "title": "Local network scan",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the monkey should scan its subnets additionally"
                        },
                        "depth": {
                            "title": "Distance from island",
                            "type": "integer",
                            "default": 2,
                            "description":
                                "Amount of hops allowed for the monkey to spread from the island. "
                                + WARNING_SIGN
                                + " Note that setting this value too high may result in the monkey propagating too far"
                        },
                        "subnet_scan_list": {
                            "title": "Scan IP/subnet list",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                            ],
                            "description":
                                "List of IPs/subnets/hosts the monkey should scan."
                                " Examples: \"192.168.0.1\", \"192.168.0.5-192.168.0.20\", \"192.168.0.5/24\","
                                " \"printer.example\""
                        }
                    }
                },
                "network_analysis": {
                    "title": "Network Analysis",
                    "type": "object",
                    "properties": {
                        "inaccessible_subnets": {
                            "title": "Network segmentation testing",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                            ],
                            "description":
                                "Test for network segmentation by providing a list of"
                                " subnets that should NOT be accessible to each other."
                                " For example, given the following configuration:"
                                " '10.0.0.0/24, 11.0.0.2/32, 12.2.3.0/24'"
                                " a Monkey running on 10.0.0.5 will try to access machines in the following"
                                " subnets: 11.0.0.2/32, 12.2.3.0/24."
                                " An alert on successful connections will be shown in the report"
                                " Additional subnet formats include: 13.0.0.1, 13.0.0.1-13.0.0.5"
                        }
                    }
                }
            }
        },
        "monkey": {
            "title": "Monkey",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "alive": {
                            "title": "Alive",
                            "type": "boolean",
                            "default": True,
                            "description": "Is the monkey alive"
                        },
                        "post_breach_actions": {
                            "title": "Post breach actions",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "$ref": "#/definitions/post_breach_acts"
                            },
                            "default": [
                            ],
                            "description": "List of actions the Monkey will run post breach"
                        },
                    }
                },
                "behaviour": {
                    "title": "Behaviour",
                    "type": "object",
                    "properties": {
                        "custom_PBA_linux_cmd": {
                            "title": "Linux post breach command",
                            "type": "string",
                            "default": "",
                            "description": "Linux command to be executed after breaching."
                        },
                        "PBA_linux_file": {
                            "title": "Linux post breach file",
                            "type": "string",
                            "format": "data-url",
                            "description": "File to be executed after breaching. "
                                           "If you want custom execution behavior, "
                                           "specify it in 'Linux post breach command' field. "
                                           "Reference your file by filename."
                        },
                        "custom_PBA_windows_cmd": {
                            "title": "Windows post breach command",
                            "type": "string",
                            "default": "",
                            "description": "Windows command to be executed after breaching."
                        },
                        "PBA_windows_file": {
                            "title": "Windows post breach file",
                            "type": "string",
                            "format": "data-url",
                            "description": "File to be executed after breaching. "
                                           "If you want custom execution behavior, "
                                           "specify it in 'Windows post breach command' field. "
                                           "Reference your file by filename."
                        },
                        "PBA_windows_filename": {
                            "title": "Windows PBA filename",
                            "type": "string",
                            "default": ""
                        },
                        "PBA_linux_filename": {
                            "title": "Linux PBA filename",
                            "type": "string",
                            "default": ""
                        },
                        "self_delete_in_cleanup": {
                            "title": "Self delete on cleanup",
                            "type": "boolean",
                            "default": False,
                            "description": "Should the monkey delete its executable when going down"
                        },
                        "use_file_logging": {
                            "title": "Use file logging",
                            "type": "boolean",
                            "default": True,
                            "description": "Should the monkey dump to a log file"
                        },
                        "serialize_config": {
                            "title": "Serialize config",
                            "type": "boolean",
                            "default": False,
                            "description": "Should the monkey dump its config on startup"
                        }
                    }
                },
                "system_info": {
                    "title": "System info",
                    "type": "object",
                    "properties": {
                        "extract_azure_creds": {
                            "title": "Harvest Azure Credentials",
                            "type": "boolean",
                            "default": True,
                            "attack_techniques": ["T1003", "T1078"],
                            "description":
                                "Determine if the Monkey should try to harvest password credentials from Azure VMs"
                        },
                        "collect_system_info": {
                            "title": "Collect system info",
                            "type": "boolean",
                            "default": True,
                            "attack_techniques": ["T1082"],
                            "description": "Determines whether to collect system info"
                        },
                        "should_use_mimikatz": {
                            "title": "Should use Mimikatz",
                            "type": "boolean",
                            "default": True,
                            "attack_techniques": ["T1003", "T1078"],
                            "description": "Determines whether to use Mimikatz"
                        },
                    }
                },
                "life_cycle": {
                    "title": "Life cycle",
                    "type": "object",
                    "properties": {
                        "max_iterations": {
                            "title": "Max iterations",
                            "type": "integer",
                            "default": 1,
                            "description": "Determines how many iterations of the monkey's full lifecycle should occur"
                        },
                        "victims_max_find": {
                            "title": "Max victims to find",
                            "type": "integer",
                            "default": 30,
                            "description": "Determines the maximum number of machines the monkey is allowed to scan"
                        },
                        "victims_max_exploit": {
                            "title": "Max victims to exploit",
                            "type": "integer",
                            "default": 7,
                            "description":
                                "Determines the maximum number of machines the monkey"
                                " is allowed to successfully exploit. " + WARNING_SIGN
                                + " Note that setting this value too high may result in the monkey propagating to "
                                  "a high number of machines"
                        },
                        "timeout_between_iterations": {
                            "title": "Wait time between iterations",
                            "type": "integer",
                            "default": 100,
                            "description":
                                "Determines for how long (in seconds) should the monkey wait between iterations"
                        },
                        "retry_failed_explotation": {
                            "title": "Retry failed exploitation",
                            "type": "boolean",
                            "default": True,
                            "description":
                                "Determines whether the monkey should retry exploiting machines"
                                " it didn't successfuly exploit on previous iterations"
                        }
                    }
                }
            }
        },
        "internal": {
            "title": "Internal",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "singleton_mutex_name": {
                            "title": "Singleton mutex name",
                            "type": "string",
                            "default": "{2384ec59-0df8-4ab9-918c-843740924a28}",
                            "description":
                                "The name of the mutex used to determine whether the monkey is already running"
                        },
                        "keep_tunnel_open_time": {
                            "title": "Keep tunnel open time",
                            "type": "integer",
                            "default": 60,
                            "description": "Time to keep tunnel open before going down after last exploit (in seconds)"
                        },
                        "monkey_dir_name": {
                            "title": "Monkey's directory name",
                            "type": "string",
                            "default": r"monkey_dir",
                            "description": "Directory name for the directory which will contain all of the monkey files"
                        },
                    }
                },
                "classes": {
                    "title": "Classes",
                    "type": "object",
                    "properties": {
                        "finger_classes": {
                            "title": "Fingerprint classes",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "$ref": "#/definitions/finger_classes"
                            },
                            "default": [
                                "SMBFinger",
                                "SSHFinger",
                                "PingScanner",
                                "HTTPFinger",
                                "MySQLFinger",
                                "MSSQLFinger",
                                "ElasticFinger"
                            ],
                            "description": "Determines which classes to use for fingerprinting"
                        }
                    }
                },
                "kill_file": {
                    "title": "Kill file",
                    "type": "object",
                    "properties": {
                        "kill_file_path_windows": {
                            "title": "Kill file path on Windows",
                            "type": "string",
                            "default": "%windir%\\monkey.not",
                            "description": "Path of file which kills monkey if it exists (on Windows)"
                        },
                        "kill_file_path_linux": {
                            "title": "Kill file path on Linux",
                            "type": "string",
                            "default": "/var/run/monkey.not",
                            "description": "Path of file which kills monkey if it exists (on Linux)"
                        }
                    }
                },
                "dropper": {
                    "title": "Dropper",
                    "type": "object",
                    "properties": {
                        "dropper_set_date": {
                            "title": "Dropper sets date",
                            "type": "boolean",
                            "default": True,
                            "description":
                                "Determines whether the dropper should set the monkey's file date to be the same as"
                                " another file"
                        },
                        "dropper_date_reference_path_windows": {
                            "title": "Dropper date reference path (Windows)",
                            "type": "string",
                            "default": "%windir%\\system32\\kernel32.dll",
                            "description":
                                "Determines which file the dropper should copy the date from if it's configured to do"
                                " so on Windows (use fullpath)"
                        },
                        "dropper_date_reference_path_linux": {
                            "title": "Dropper date reference path (Linux)",
                            "type": "string",
                            "default": "/bin/sh",
                            "description":
                                "Determines which file the dropper should copy the date from if it's configured to do"
                                " so on Linux (use fullpath)"
                        },
                        "dropper_target_path_linux": {
                            "title": "Dropper target path on Linux",
                            "type": "string",
                            "default": "/tmp/monkey",
                            "description": "Determines where should the dropper place the monkey on a Linux machine"
                        },
                        "dropper_target_path_win_32": {
                            "title": "Dropper target path on Windows (32bit)",
                            "type": "string",
                            "default": "C:\\Windows\\temp\\monkey32.exe",
                            "description": "Determines where should the dropper place the monkey on a Windows machine "
                                           "(32bit)"
                        },
                        "dropper_target_path_win_64": {
                            "title": "Dropper target path on Windows (64bit)",
                            "type": "string",
                            "default": "C:\\Windows\\temp\\monkey64.exe",
                            "description": "Determines where should the dropper place the monkey on a Windows machine "
                                           "(64 bit)"
                        },
                        "dropper_try_move_first": {
                            "title": "Try to move first",
                            "type": "boolean",
                            "default": True,
                            "description":
                                "Determines whether the dropper should try to move itsel instead of copying itself"
                                " to target path"
                        }
                    }
                },
                "logging": {
                    "title": "Logging",
                    "type": "object",
                    "properties": {
                        "dropper_log_path_linux": {
                            "title": "Dropper log file path on Linux",
                            "type": "string",
                            "default": "/tmp/user-1562",
                            "description": "The fullpath of the dropper log file on Linux"
                        },
                        "dropper_log_path_windows": {
                            "title": "Dropper log file path on Windows",
                            "type": "string",
                            "default": "%temp%\\~df1562.tmp",
                            "description": "The fullpath of the dropper log file on Windows"
                        },
                        "monkey_log_path_linux": {
                            "title": "Monkey log file path on Linux",
                            "type": "string",
                            "default": "/tmp/user-1563",
                            "description": "The fullpath of the monkey log file on Linux"
                        },
                        "monkey_log_path_windows": {
                            "title": "Monkey log file path on Windows",
                            "type": "string",
                            "default": "%temp%\\~df1563.tmp",
                            "description": "The fullpath of the monkey log file on Windows"
                        },
                        "send_log_to_server": {
                            "title": "Send log to server",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the monkey sends its log to the Monkey Island server"
                        }
                    }
                },
                "exploits": {
                    "title": "Exploits",
                    "type": "object",
                    "properties": {
                        "exploit_lm_hash_list": {
                            "title": "Exploit LM hash list",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [],
                            "description": "List of LM hashes to use on exploits using credentials"
                        },
                        "exploit_ntlm_hash_list": {
                            "title": "Exploit NTLM hash list",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [],
                            "description": "List of NTLM hashes to use on exploits using credentials"
                        },
                        "exploit_ssh_keys": {
                            "title": "SSH key pairs list",
                            "type": "array",
                            "uniqueItems": True,
                            "default": [],
                            "items": {
                                "type": "string"
                            },
                            "description": "List of SSH key pairs to use, when trying to ssh into servers"
                        }
                    }
                }
            }
        },
        "cnc": {
            "title": "Monkey Island",
            "type": "object",
            "properties": {
                "servers": {
                    "title": "Servers",
                    "type": "object",
                    "properties": {
                        "command_servers": {
                            "title": "Command servers",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                                "192.0.2.0:5000"
                            ],
                            "description": "List of command servers to try and communicate with (format is <ip>:<port>)"
                        },
                        "internet_services": {
                            "title": "Internet services",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                                "monkey.guardicore.com",
                                "www.google.com"
                            ],
                            "description":
                                "List of internet services to try and communicate with to determine internet"
                                " connectivity (use either ip or domain)"
                        },
                        "current_server": {
                            "title": "Current server",
                            "type": "string",
                            "default": "192.0.2.0:5000",
                            "description": "The current command server the monkey is communicating with"
                        }
                    }
                },
            }
        },
        "exploits": {
            "title": "Exploits",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "exploiter_classes": {
                            "title": "Exploits",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "$ref": "#/definitions/exploiter_classes"
                            },
                            "default": [
                                "SmbExploiter",
                                "WmiExploiter",
                                "SSHExploiter",
                                "ShellShockExploiter",
                                "SambaCryExploiter",
                                "ElasticGroovyExploiter",
                                "Struts2Exploiter",
                                "WebLogicExploiter",
                                "HadoopExploiter",
                                "VSFTPDExploiter"
                            ],
                            "description":
                                "Determines which exploits to use. " + WARNING_SIGN
                                + " Note that using unsafe exploits may cause crashes of the exploited machine/service"
                        },
                        "skip_exploit_if_file_exist": {
                            "title": "Skip exploit if file exists",
                            "type": "boolean",
                            "default": False,
                            "description": "Determines whether the monkey should skip the exploit if the monkey's file"
                                           " is already on the remote machine"
                        }
                    }
                },
                "ms08_067": {
                    "title": "MS08_067",
                    "type": "object",
                    "properties": {
                        "ms08_067_exploit_attempts": {
                            "title": "MS08_067 exploit attempts",
                            "type": "integer",
                            "default": 5,
                            "description": "Number of attempts to exploit using MS08_067"
                        },
                        "user_to_add": {
                            "title": "Remote user",
                            "type": "string",
                            "default": "Monkey_IUSER_SUPPORT",
                            "description": "Username to add on successful exploit"
                        },
                        "remote_user_pass": {
                            "title": "Remote user password",
                            "type": "string",
                            "default": "Password1!",
                            "description": "Password to use for created user"
                        }
                    }
                },
                "rdp_grinder": {
                    "title": "RDP grinder",
                    "type": "object",
                    "properties": {
                        "rdp_use_vbs_download": {
                            "title": "Use VBS download",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether to use VBS or BITS to download monkey to remote machine"
                                           " (true=VBS, false=BITS)"
                        }
                    }
                },
                "sambacry": {
                    "title": "SambaCry",
                    "type": "object",
                    "properties": {
                        "sambacry_trigger_timeout": {
                            "title": "SambaCry trigger timeout",
                            "type": "integer",
                            "default": 5,
                            "description": "Timeout (in seconds) of SambaCry trigger"
                        },
                        "sambacry_folder_paths_to_guess": {
                            "title": "SambaCry folder paths to guess",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                                '/',
                                '/mnt',
                                '/tmp',
                                '/storage',
                                '/export',
                                '/share',
                                '/shares',
                                '/home'
                            ],
                            "description": "List of full paths to share folder for SambaCry to guess"
                        },
                        "sambacry_shares_not_to_check": {
                            "title": "SambaCry shares not to check",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                                "IPC$", "print$"
                            ],
                            "description": "These shares won't be checked when exploiting with SambaCry"
                        }
                    }
                },
                "smb_service": {
                    "title": "SMB service",
                    "type": "object",
                    "properties": {
                        "smb_download_timeout": {
                            "title": "SMB download timeout",
                            "type": "integer",
                            "default": 300,
                            "description":
                                "Timeout (in seconds) for SMB download operation (used in various exploits using SMB)"
                        },
                        "smb_service_name": {
                            "title": "SMB service name",
                            "type": "string",
                            "default": "InfectionMonkey",
                            "description": "Name of the SMB service that will be set up to download monkey"
                        }
                    }
                }
            }
        },
        "network": {
            "title": "Network",
            "type": "object",
            "properties": {
                "tcp_scanner": {
                    "title": "TCP scanner",
                    "type": "object",
                    "properties": {
                        "HTTP_PORTS": {
                            "title": "HTTP ports",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "integer"
                            },
                            "default": [
                                80,
                                8080,
                                443,
                                8008,
                                7001
                            ],
                            "description": "List of ports the monkey will check if are being used for HTTP"
                        },
                        "tcp_target_ports": {
                            "title": "TCP target ports",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "integer"
                            },
                            "default": [
                                22,
                                2222,
                                445,
                                135,
                                3389,
                                80,
                                8080,
                                443,
                                8008,
                                3306,
                                9200,
                                7001
                            ],
                            "description": "List of TCP ports the monkey will check whether they're open"
                        },
                        "tcp_scan_interval": {
                            "title": "TCP scan interval",
                            "type": "integer",
                            "default": 0,
                            "description": "Time to sleep (in milliseconds) between scans"
                        },
                        "tcp_scan_timeout": {
                            "title": "TCP scan timeout",
                            "type": "integer",
                            "default": 3000,
                            "description": "Maximum time (in milliseconds) to wait for TCP response"
                        },
                        "tcp_scan_get_banner": {
                            "title": "TCP scan - get banner",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the TCP scan should try to get the banner"
                        }
                    }
                },
                "ping_scanner": {
                    "title": "Ping scanner",
                    "type": "object",
                    "properties": {
                        "ping_scan_timeout": {
                            "title": "Ping scan timeout",
                            "type": "integer",
                            "default": 1000,
                            "description": "Maximum time (in milliseconds) to wait for ping response"
                        }
                    }
                }
            }
        }
    },
    "options": {
        "collapsed": True
    }
}
