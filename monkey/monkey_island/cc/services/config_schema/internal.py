INTERNAL = {
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
                "started_on_island": {
                    "title": "Started on island",
                    "type": "boolean",
                    "default": False,
                    "description": "Was exploitation started from island"
                                   "(did monkey with max depth ran on island)"
                },
            }
        },
        "monkey": {
            "title": "Monkey",
            "type": "object",
            "properties": {
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
                "self_delete_in_cleanup": {
                    "title": "Self delete on cleanup",
                    "type": "boolean",
                    "default": True,
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
                },
                "alive": {
                    "title": "Alive",
                    "type": "boolean",
                    "default": True,
                    "description": "Is the monkey alive"
                }
            }
        },
        "island_server": {
            "title": "Island server",
            "type": "object",
            "properties": {
                "command_servers": {
                    "title": "Island server's IP's",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string"
                    },
                    "default": [
                        "192.0.2.0:5000"
                    ],
                    "description": "List of command servers/network interfaces to try to communicate with "
                                   "(format is <ip>:<port>)"
                },
                "current_server": {
                    "title": "Current server",
                    "type": "string",
                    "default": "192.0.2.0:5000",
                    "description": "The current command server the monkey is communicating with"
                }
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
                    ]
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
                        "Determines whether the dropper should try to move itself instead of copying itself"
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
        },
        "testing": {
            "title": "Testing",
            "type": "object",
            "properties": {
                "export_monkey_telems": {
                    "title": "Export monkey telemetries",
                    "type": "boolean",
                    "default": False,
                    "description": "Exports unencrypted telemetries that can be used for tests in development."
                                   " Do not turn on!"
                }
            }
        }
    }
}
