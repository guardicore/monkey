INTERNAL = {
    "title": "Internal",
    "type": "object",
    "properties": {
        "general": {
            "title": "General",
            "type": "object",
            "properties": {
                "keep_tunnel_open_time": {
                    "title": "Keep tunnel open time",
                    "type": "integer",
                    "default": 60,
                    "description": "Time to keep tunnel open before going down after last exploit "
                    "(in seconds)",
                },
            },
        },
        "monkey": {
            "title": "Monkey",
            "type": "object",
            "properties": {
                "alive": {
                    "title": "Alive",
                    "type": "boolean",
                    "default": True,
                    "description": "Is the monkey alive",
                },
                "aws_keys": {
                    "type": "object",
                    "properties": {
                        "aws_access_key_id": {"type": "string", "default": ""},
                        "aws_secret_access_key": {"type": "string", "default": ""},
                        "aws_session_token": {"type": "string", "default": ""},
                    },
                },
            },
        },
        "island_server": {
            "title": "Island server",
            "type": "object",
            "properties": {
                "command_servers": {
                    "title": "Island server's IP's",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string"},
                    "default": ["192.0.2.0:5000"],
                    "description": "List of command servers/network interfaces to try to "
                    "communicate with "
                    "(format is <ip>:<port>)",
                },
                "current_server": {
                    "title": "Current server",
                    "type": "string",
                    "default": "192.0.2.0:5000",
                    "description": "The current command server the monkey is communicating with",
                },
            },
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
                            "items": {"type": "integer"},
                            "default": [80, 8080, 443, 8008, 7001, 9200],
                            "description": "List of ports the monkey will check if are being used "
                            "for HTTP",
                        },
                        "tcp_target_ports": {
                            "title": "TCP target ports",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {"type": "integer"},
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
                                7001,
                                8088,
                            ],
                            "description": "List of TCP ports the monkey will check whether "
                            "they're open",
                        },
                        "tcp_scan_interval": {
                            "title": "TCP scan interval",
                            "type": "integer",
                            "default": 0,
                            "description": "Time to sleep (in milliseconds) between scans",
                        },
                        "tcp_scan_timeout": {
                            "title": "TCP scan timeout",
                            "type": "integer",
                            "default": 3000,
                            "description": "Maximum time (in milliseconds) "
                            "to wait for TCP response",
                        },
                        "tcp_scan_get_banner": {
                            "title": "TCP scan - get banner",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the TCP scan should try to get the "
                            "banner",
                        },
                    },
                },
                "ping_scanner": {
                    "title": "Ping scanner",
                    "type": "object",
                    "properties": {
                        "ping_scan_timeout": {
                            "title": "Ping scan timeout",
                            "type": "integer",
                            "default": 1000,
                            "description": "Maximum time (in milliseconds) to wait for ping "
                            "response",
                        }
                    },
                },
            },
        },
        "classes": {
            "title": "Classes",
            "type": "object",
            "properties": {
                "finger_classes": {
                    "title": "Fingerprint classes",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"$ref": "#/definitions/finger_classes"},
                    "default": [
                        "SMBFinger",
                        "SSHFinger",
                        "HTTPFinger",
                        "MSSQLFinger",
                        "ElasticFinger",
                    ],
                }
            },
        },
        "dropper": {
            "title": "Dropper",
            "type": "object",
            "properties": {
                "dropper_set_date": {
                    "title": "Dropper sets date",
                    "type": "boolean",
                    "default": True,
                    "description": "Determines whether the dropper should set the monkey's file "
                    "date to be the same as"
                    " another file",
                },
                "dropper_date_reference_path_windows": {
                    "title": "Dropper date reference path (Windows)",
                    "type": "string",
                    "default": "%windir%\\system32\\kernel32.dll",
                    "description": "Determines which file the dropper should copy the date from if "
                    "it's configured to do"
                    " so on Windows (use fullpath)",
                },
                "dropper_date_reference_path_linux": {
                    "title": "Dropper date reference path (Linux)",
                    "type": "string",
                    "default": "/bin/sh",
                    "description": "Determines which file the dropper should copy the date from if "
                    "it's configured to do"
                    " so on Linux (use fullpath)",
                },
                "dropper_target_path_linux": {
                    "title": "Dropper target path on Linux",
                    "type": "string",
                    "default": "/tmp/monkey",
                    "description": "Determines where should the dropper place the monkey on a "
                    "Linux machine",
                },
                "dropper_target_path_win_32": {
                    "title": "Dropper target path on Windows (32bit)",
                    "type": "string",
                    "default": "C:\\Windows\\temp\\monkey32.exe",
                    "description": "Determines where should the dropper place the monkey on a "
                    "Windows machine "
                    "(32bit)",
                },
                "dropper_target_path_win_64": {
                    "title": "Dropper target path on Windows (64bit)",
                    "type": "string",
                    "default": "C:\\Windows\\temp\\monkey64.exe",
                    "description": "Determines where should the dropper place the monkey on a "
                    "Windows machine "
                    "(64 bit)",
                },
            },
        },
        "logging": {
            "title": "Logging",
            "type": "object",
            "properties": {
                "dropper_log_path_linux": {
                    "title": "Dropper log file path on Linux",
                    "type": "string",
                    "default": "/tmp/user-1562",
                    "description": "The fullpath of the dropper log file on Linux",
                },
                "dropper_log_path_windows": {
                    "title": "Dropper log file path on Windows",
                    "type": "string",
                    "default": "%temp%\\~df1562.tmp",
                    "description": "The fullpath of the dropper log file on Windows",
                },
                "monkey_log_path_linux": {
                    "title": "Monkey log file path on Linux",
                    "type": "string",
                    "default": "/tmp/user-1563",
                    "description": "The fullpath of the monkey log file on Linux",
                },
                "monkey_log_path_windows": {
                    "title": "Monkey log file path on Windows",
                    "type": "string",
                    "default": "%temp%\\~df1563.tmp",
                    "description": "The fullpath of the monkey log file on Windows",
                },
            },
        },
        "exploits": {
            "title": "Exploits",
            "type": "object",
            "properties": {
                "exploit_lm_hash_list": {
                    "title": "Exploit LM hash list",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string"},
                    "default": [],
                    "description": "List of LM hashes to use on exploits using credentials",
                    "related_attack_techniques": ["T1075"],
                },
                "exploit_ntlm_hash_list": {
                    "title": "Exploit NTLM hash list",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string"},
                    "default": [],
                    "description": "List of NTLM hashes to use on exploits using credentials",
                    "related_attack_techniques": ["T1075"],
                },
                "exploit_ssh_keys": {
                    "title": "SSH key pairs list",
                    "type": "array",
                    "uniqueItems": True,
                    "default": [],
                    "items": {"type": "string"},
                    "description": "List of SSH key pairs to use, when trying to ssh into servers",
                },
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "skip_exploit_if_file_exist": {
                            "title": "Skip exploit if file exists",
                            "type": "boolean",
                            "default": False,
                            "description": "Determines whether the monkey should skip the exploit "
                            "if the monkey's file"
                            " is already on the remote machine",
                        }
                    },
                },
                "ms08_067": {
                    "title": "MS08_067",
                    "type": "object",
                    "properties": {
                        "ms08_067_exploit_attempts": {
                            "title": "MS08_067 exploit attempts",
                            "type": "integer",
                            "default": 5,
                            "description": "Number of attempts to exploit using MS08_067",
                        },
                        "user_to_add": {
                            "title": "Remote user",
                            "type": "string",
                            "default": "Monkey_IUSER_SUPPORT",
                            "description": "Username to add on successful exploit",
                        },
                    },
                },
            },
            "smb_service": {
                "title": "SMB service",
                "type": "object",
                "properties": {
                    "smb_download_timeout": {
                        "title": "SMB download timeout",
                        "type": "integer",
                        "default": 300,
                        "description": "Timeout (in seconds) for SMB download operation (used in "
                        "various exploits using SMB)",
                    },
                    "smb_service_name": {
                        "title": "SMB service name",
                        "type": "string",
                        "default": "InfectionMonkey",
                        "description": "Name of the SMB service that will be set up to download "
                        "monkey",
                    },
                },
            },
        },
        "testing": {
            "title": "Testing",
            "type": "object",
            "properties": {
                "export_monkey_telems": {
                    "title": "Export monkey telemetries",
                    "type": "boolean",
                    "default": False,
                    "description": "Exports unencrypted telemetries that "
                    "can be used for tests in development."
                    " Do not turn on!",
                }
            },
        },
    },
}
