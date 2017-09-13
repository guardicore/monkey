import json

from flask import request, jsonify
import flask_restful

from cc.database import mongo

__author__ = 'Barak'


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
                  "title": "SmbExploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "WmiExploiter"
                  ],
                  "title": "WmiExploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "RdpExploiter"
                  ],
                  "title": "RdpExploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "Ms08_067_Exploiter"
                  ],
                  "title": "Ms08_067_Exploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "SSHExploiter"
                  ],
                  "title": "SSHExploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "ShellShockExploiter"
                  ],
                  "title": "ShellShockExploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "SambaCryExploiter"
                  ],
                  "title": "SambaCryExploiter"
                }
            ]
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
                  "title": "SMBFinger"
                },
                {
                  "type": "string",
                  "enum": [
                    "SSHFinger"
                  ],
                  "title": "SSHFinger"
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
                }
            ]
        }
    },
    "properties": {
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
                        "depth": {
                            "title": "Depth",
                            "type": "integer",
                            "default": 2,
                            "description": "Amount of hops allowed from this monkey to spread"
                        }
                    }
                },
                "behaviour": {
                    "title": "Behaviour",
                    "type": "object",
                    "properties": {
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
                            "default": 14,
                            "description": "Determines after how many discovered machines should the monkey stop scanning"
                        },
                        "victims_max_exploit": {
                            "title": "Max victims to exploit",
                            "type": "integer",
                            "default": 7,
                            "description": "Determines after how many infected machines should the monkey stop infecting"
                        },
                        "timeout_between_iterations": {
                            "title": "Wait time between iterations",
                            "type": "integer",
                            "default": 100,
                            "description": "Determines for how long (in seconds) should the monkey wait between iterations"
                        },
                        "retry_failed_explotation": {
                            "title": "Retry failed exploitation",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the monkey should retry exploiting machines it didn't successfuly exploit on previous iterations"
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
                            "description": "The name of the mutex used to determine whether the monkey is already running"
                        }
                    }
                },
                "classes": {
                    "title": "Classes",
                    "type": "object",
                    "properties": {
                        "scanner_class": {
                            "title": "Scanner class",
                            "type": "string",
                            "default": "TcpScanner",
                            "enum": [
                                "TcpScanner"
                            ],
                            "enumNames": [
                                "TcpScanner"
                            ],
                            "description": "Determines class to scan for machines. (Shouldn't be changed)"
                        },
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
                                "HTTPFinger"
                            ],
                            "description": "Determines which classes to use for fingerprinting"
                        },
                        "exploiter_classes": {
                            "title": "Exploiter classes",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "$ref": "#/definitions/exploiter_classes"
                            },
                            "default": [
                                "SmbExploiter",
                                "WmiExploiter",
                                "RdpExploiter",
                                "Ms08_067_Exploiter",
                                "SSHExploiter",
                                "ShellShockExploiter",
                                "SambaCryExploiter"
                            ],
                            "description": "Determines which classes to use for exploiting"
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
                            "default": "C:\\Windows\\monkey.not",
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
                            "description": "Determines whether the dropper should set the monkey's file date to be the same as another file"
                        },
                        "dropper_date_reference_path": {
                            "title": "Droper date reference path",
                            "type": "string",
                            "default": "\\windows\\system32\\kernel32.dll",
                            "description": "Determines which file the dropper should copy the date from if it's configured to do so (use fullpath)"
                        },
                        "dropper_target_path_linux": {
                            "title": "Dropper target path on Linux",
                            "type": "string",
                            "default": "/tmp/monkey",
                            "description": "Determines where should the dropper place the monkey on a Linux machine"
                        },
                        "dropper_target_path": {
                            "title": "Dropper target path on Windows",
                            "type": "string",
                            "default": "C:\\Windows\\monkey.exe",
                            "description": "Determines where should the dropper place the monkey on a Windows machine"
                        },
                        "dropper_try_move_first": {
                            "title": "Try to move first",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the dropper should try to move itself instead of copying itself to target path"
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
                            "default": "C:\\Users\\user\\AppData\\Local\\Temp\\~df1562.tmp",
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
                            "default":"C:\\Users\\user\\AppData\\Local\\Temp\\~df1563.tmp",
                            "description": "The fullpath of the monkey log file on Windows"
                        }
                    }
                }
            }
        },
        "cnc": {
            "title": "C&C",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                    }
                },
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
                                "41.50.73.31:5000"
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
                            "description": "List of internet services to try and communicate with to determine internet connectivity (use either ip or domain)"
                        },
                        "current_server": {
                            "title": "Current server",
                            "type": "string",
                            "default": "41.50.73.31:5000",
                            "description": "The current command server the monkey is communicating with"
                        }
                    }
                }
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
                        "skip_exploit_if_file_exist": {
                            "title": "Skip exploit if file exists",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether the monkey should skip the exploit if the monkey's file is already on the remote machine"
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
                        "ms08_067_remote_user_add": {
                            "title": "MS08_067 remote user",
                            "type": "string",
                            "default": "Monkey_IUSER_SUPPORT",
                            "description": "Username to add on successful exploit"
                        },
                        "ms08_067_remote_user_pass": {
                            "title": "MS08_067 remote user password",
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
                            "description": "Determines whether to use VBS or BITS to download monkey to remote machine (true=VBS, false=BITS)"
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
                        },
                        "sambacry_commandline_filename": {
                            "title": "SambaCry commandline filename",
                            "type": "string",
                            "default": "monkey_commandline.txt",
                        },
                        "sambacry_runner_result_filename": {
                            "title": "SambaCry runner result filename",
                            "type": "string",
                            "default": "monkey_runner_result",
                        },
                        "sambacry_runner_filename_32": {
                            "title": "SambaCry runner filename (32 bit)",
                            "type": "string",
                            "default": "sc_monkey_runner32.so",
                        },
                        "sambacry_runner_filename_64": {
                            "title": "SambaCry runner filename (64 bit)",
                            "type": "string",
                            "default": "sc_monkey_runner64.so",
                        },
                        "sambacry_monkey_filename_32": {
                            "title": "SambaCry monkey filename (32 bit)",
                            "type": "string",
                            "default": "monkey32",
                        },
                        "sambacry_monkey_filename_64": {
                            "title": "SambaCry monkey filename (64 bit)",
                            "type": "string",
                            "default": "monkey64",
                        },
                        "sambacry_monkey_copy_filename_32": {
                            "title": "SambaCry monkey copy filename (32 bit)",
                            "type": "string",
                            "default": "monkey32_2",
                        },
                        "sambacry_monkey_copy_filename_64": {
                            "title": "SambaCry monkey copy filename (64 bit)",
                            "type": "string",
                            "default": "monkey64_2",
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
                            "description": "Timeout (in seconds) for SMB download operation (used in various exploits using SMB)"
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
        "system_info": {
            "title": "System info",
            "type": "object",
            "properties": {
                "general": {
                    "title": "General",
                    "type": "object",
                    "properties": {
                        "collect_system_info": {
                            "title": "Collect system info",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether to collect system info"
                        }
                    }
                },
                "mimikatz": {
                    "title": "Mimikatz",
                    "type": "object",
                    "properties": {
                        "mimikatz_dll_name": {
                            "title": "Mimikatz DLL name",
                            "type": "string",
                            "default": "mk.dll",
                            "description": "Name of Mimikatz DLL (should be the same as in the monkey's pyinstaller spec file)"
                        }
                    }
                }
            }
        },
        "network": {
            "title": "Network",
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
                            "default": False,
                            "description": "Determines whether monkey should also scan its own IPs"
                        },
                        "network_range": {
                            "title": "Network range",
                            "type": "object",
                            "properties": {
                                "range_class": {
                                    "title": "Range class",
                                    "type": "string",
                                    "default": "FixedRange",
                                    "enum": [
                                        "FixedRange",
                                        "RelativeRange",
                                        "ClassCRange"
                                      ],
                                      "enumNames": [
                                        "FixedRange",
                                        "RelativeRange",
                                        "ClassCRange"
                                      ],
                                    "description": "Determines which class to use to determine scan range"
                                },
                                "range_size": {
                                    "title": "Relative range size",
                                    "type": "integer",
                                    "default": 1,
                                    "description": "Determines the size of the RelativeRange - amount of IPs to include"
                                },
                                "range_fixed": {
                                    "title": "Fixed range IP list",
                                    "type": "array",
                                    "uniqueItems": True,
                                    "items": {
                                        "type": "string"
                                    },
                                    "default": [
                                        "172.16.0.67"
                                    ],
                                    "description": "List of IPs to include when using FixedRange"
                                }
                            }
                        }
                    }
                },
                "scanners": {
                    "title": "Scanners",
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
                                        8008
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
                                        8008
                                    ],
                                    "description": "List of TCP ports the monkey will check whether they're open"
                                },
                                "tcp_scan_interval": {
                                    "title": "TCP scan interval",
                                    "type": "integer",
                                    "default": 200,
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
            }
        }
    },
    "options": {
        "collapsed": True
    }
}


class MonkeyConfiguration(flask_restful.Resource):
    def get(self):
        return jsonify(schema=SCHEMA, configuration=self._get_configuration())

    def post(self):
        config_json = json.loads(request.data)
        mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
        return jsonify(schema=SCHEMA, configuration=self._get_configuration())

    @classmethod
    def _get_configuration(cls):
        config = mongo.db.config.find_one({'name': 'newconfig'}) or {}
        for field in ('name', '_id'):
            config.pop(field, None)
        return config
