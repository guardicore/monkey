from cc.database import mongo
from jsonschema import Draft4Validator, validators

from cc.island_config import ISLAND_PORT
from cc.utils import local_ip_addresses

__author__ = "itay.mizeretz"

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
                  "title": "SMB Exploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "WmiExploiter"
                  ],
                  "title": "WMI Exploiter"
                },
                {
                  "type": "string",
                  "enum": [
                    "RdpExploiter"
                  ],
                  "title": "RDP Exploiter (UNSAFE)"
                },
                {
                  "type": "string",
                  "enum": [
                    "Ms08_067_Exploiter"
                  ],
                  "title": "MS08-067 Exploiter (UNSAFE)"
                },
                {
                  "type": "string",
                  "enum": [
                    "SSHExploiter"
                  ],
                  "title": "SSH Exploiter"
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
                },
                {
                  "type": "string",
                  "enum": [
                    "MySQLFinger"
                  ],
                  "title": "MySQLFinger"
                },
                {
                  "type": "string",
                  "enum": [
                    "ElasticFinger"
                  ],
                  "title": "ElasticFinger"
                }
            ]
        }
    },
    "properties": {
        "basic": {
            "title": "Basic - Credentials",
            "type": "object",
            "properties": {
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
                        }
                    }
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
                                "ClassCRange"
                            ],
                            "enumNames": [
                                "Fixed Range",
                                "Class C Range"
                            ],
                            "description":
                                "Determines which class to use to determine scan range."
                                " Fixed Range will scan only specific IPs listed under Fixed range IP list."
                                " Class C Range will scan machines in the Class C network the monkey's on."
                        },
                        "range_fixed": {
                            "title": "Fixed range IP list",
                            "type": "array",
                            "uniqueItems": True,
                            "items": {
                                "type": "string"
                            },
                            "default": [
                            ],
                            "description":
                                "List of IPs to include when using FixedRange"
                                " (Only relevant for Fixed Range)"
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
                        "collect_system_info": {
                            "title": "Collect system info",
                            "type": "boolean",
                            "default": True,
                            "description": "Determines whether to collect system info"
                        },
                        "keep_tunnel_open_time": {
                            "title": "Keep tunnel open time",
                            "type": "integer",
                            "default": 60,
                            "description": "Time to keep tunnel open before going down after last exploit (in seconds)"
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
                                "HTTPFinger",
                                "MySQLFinger",
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
                            "description":
                                "Name of Mimikatz DLL (should be the same as in the monkey's pyinstaller spec file)"
                        }
                    }
                }
            }
        },
        "cnc": {
            "title": "C&C",
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
                            "description":
                                "List of internet services to try and communicate with to determine internet"
                                " connectivity (use either ip or domain)"
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
                                "ElasticGroovyExploiter"
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
                                8008,
                                3306,
                                9200
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
    },
    "options": {
        "collapsed": True
    }
}


class ConfigService:
    def __init__(self):
        pass

    @staticmethod
    def get_config(is_initial_config=False):
        config = mongo.db.config.find_one({'name': 'initial' if is_initial_config else 'newconfig'}) or {}
        for field in ('name', '_id'):
            config.pop(field, None)
        return config

    @staticmethod
    def get_config_value(config_key_as_arr, is_initial_config=False):
        config_key = reduce(lambda x, y: x+'.'+y, config_key_as_arr)
        config = mongo.db.config.find_one({'name': 'initial' if is_initial_config else 'newconfig'}, {config_key: 1})
        for config_key_part in config_key_as_arr:
            config = config[config_key_part]
        return config

    @staticmethod
    def get_flat_config(is_initial_config=False):
        config_json = ConfigService.get_config(is_initial_config)
        flat_config_json = {}
        for i in config_json:
            for j in config_json[i]:
                for k in config_json[i][j]:
                    flat_config_json[k] = config_json[i][j][k]

        return flat_config_json

    @staticmethod
    def get_config_schema():
        return SCHEMA

    @staticmethod
    def add_item_to_config_set(item_key, item_value):
        mongo.db.config.update(
            {'name': 'newconfig'},
            {'$addToSet': {item_key: item_value}},
            upsert=False
        )

        mongo.db.monkey.update(
            {},
            {'$addToSet': {'config.' + item_key.split('.')[-1]: item_value}},
            multi=True
        )

    @staticmethod
    def creds_add_username(username):
        ConfigService.add_item_to_config_set('basic.credentials.exploit_user_list', username)

    @staticmethod
    def creds_add_password(password):
        ConfigService.add_item_to_config_set('basic.credentials.exploit_password_list', password)

    @staticmethod
    def creds_add_lm_hash(lm_hash):
        ConfigService.add_item_to_config_set('internal.exploits.exploit_lm_hash_list', lm_hash)

    @staticmethod
    def creds_add_ntlm_hash(ntlm_hash):
        ConfigService.add_item_to_config_set('internal.exploits.exploit_ntlm_hash_list', ntlm_hash)

    @staticmethod
    def update_config(config_json):
        mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)

    @staticmethod
    def get_default_config():
        defaultValidatingDraft4Validator = ConfigService._extend_config_with_default(Draft4Validator)
        config = {}
        defaultValidatingDraft4Validator(SCHEMA).validate(config)
        return config

    @staticmethod
    def init_config():
        if ConfigService.get_config() != {}:
            return
        ConfigService.reset_config()

    @staticmethod
    def reset_config():
        config = ConfigService.get_default_config()
        ConfigService.set_server_ips_in_config(config)
        ConfigService.update_config(config)

    @staticmethod
    def set_server_ips_in_config(config):
        ips = local_ip_addresses()
        config["cnc"]["servers"]["command_servers"] = ["%s:%d" % (ip, ISLAND_PORT) for ip in ips]
        config["cnc"]["servers"]["current_server"] = "%s:%d" % (ips[0], ISLAND_PORT)

    @staticmethod
    def save_initial_config_if_needed():
        if mongo.db.config.find_one({'name': 'initial'}) is not None:
            return

        initial_config = mongo.db.config.find_one({'name': 'newconfig'})
        initial_config['name'] = 'initial'
        initial_config.pop('_id')
        mongo.db.config.insert(initial_config)

    @staticmethod
    def _extend_config_with_default(validator_class):
        validate_properties = validator_class.VALIDATORS["properties"]

        def set_defaults(validator, properties, instance, schema):
            # Do it only for root.
            if instance != {}:
                return
            for property, subschema in properties.iteritems():
                main_dict = {}
                for property2, subschema2 in subschema["properties"].iteritems():
                    sub_dict = {}
                    for property3, subschema3 in subschema2["properties"].iteritems():
                        if "default" in subschema3:
                            sub_dict[property3] = subschema3["default"]
                    main_dict[property2] = sub_dict
                instance.setdefault(property, main_dict)

            for error in validate_properties(validator, properties, instance, schema):
                yield error

        return validators.extend(
            validator_class, {"properties": set_defaults},
        )
