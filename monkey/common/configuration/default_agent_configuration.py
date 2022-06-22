from . import AgentConfiguration, AgentConfigurationSchema

DEFAULT_AGENT_CONFIGURATION_JSON = """{
        "keep_tunnel_open_time": 30,
        "post_breach_actions": [
            {
                "name": "CommunicateAsBackdoorUser",
                "options": {}
            },
            {
                "name": "ModifyShellStartupFiles",
                "options": {}
            },
            {
                "name": "HiddenFiles",
                "options": {}
            },
            {
                "name": "TrapCommand",
                "options": {}
            },
            {
                "name": "ChangeSetuidSetgid",
                "options": {}
            },
            {
                "name": "ScheduleJobs",
                "options": {}
            },
            {
                "name": "Timestomping",
                "options": {}
            },
            {
                "name": "AccountDiscovery",
                "options": {}
            },
            {
                "name": "ProcessListCollection",
                "options": {}
            }
        ],
        "credential_collectors": [
            {
                "name": "MimikatzCollector",
                "options": {}
            },
            {
                "name": "SSHCollector",
                "options": {}
            }
        ],
        "payloads": [
            {
                "name": "ransomware",
                "options": {
                    "encryption": {
                        "enabled": true,
                        "directories": {
                            "linux_target_dir": "",
                            "windows_target_dir": ""
                        }
                    },
                    "other_behaviors": {
                        "readme": true
                    }
                }
            }
        ],
        "custom_pbas": {
            "linux_command": "",
            "linux_filename": "",
            "windows_command": "",
            "windows_filename": ""
        },
        "propagation": {
            "maximum_depth": 2,
            "network_scan": {
                "tcp": {
                    "timeout": 3000,
                    "ports": [
                        22,
                        80,
                        135,
                        443,
                        445,
                        2222,
                        3306,
                        3389,
                        5985,
                        5986,
                        7001,
                        8008,
                        8080,
                        8088,
                        8983,
                        9200,
                        9600
                    ]
                },
                "icmp": {
                    "timeout": 1000
                },
                "fingerprinters": [
                    {
                        "name": "elastic",
                        "options": {}
                    },
                    {
                        "name": "http",
                        "options": {
                            "http_ports": [
                                80,
                                443,
                                7001,
                                8008,
                                8080,
                                8983,
                                9200,
                                9600
                            ]
                        }
                    },
                    {
                        "name": "mssql",
                        "options": {}
                    },
                    {
                        "name": "smb",
                        "options": {}
                    },
                    {
                        "name": "ssh",
                        "options": {}
                    }
                ],
                "targets": {
                    "blocked_ips": [],
                    "inaccessible_subnets": [],
                    "local_network_scan": true,
                    "subnets": []
                }
            },
            "exploitation": {
                "options": {
                    "http_ports": [
                        80,
                        443,
                        7001,
                        8008,
                        8080,
                        8983,
                        9200,
                        9600
                    ]
                },
                "brute_force": [
                    {
                        "name": "MSSQLExploiter",
                        "options": {},
                        "supported_os": [
                            "WINDOWS"
                        ]
                    },
                    {
                        "name": "PowerShellExploiter",
                        "options": {},
                        "supported_os": [
                            "WINDOWS"
                        ]
                    },
                    {
                        "name": "SSHExploiter",
                        "options": {},
                        "supported_os": [
                            "LINUX"
                        ]
                    },
                    {
                        "name": "SmbExploiter",
                        "options": {
                            "smb_download_timeout": 30
                        },
                        "supported_os": [
                            "WINDOWS"
                        ]
                    },
                    {
                        "name": "WmiExploiter",
                        "options": {
                            "smb_download_timeout": 30
                        },
                        "supported_os": [
                            "WINDOWS"
                        ]
                    }
                ],
                "vulnerability": [
                    {
                        "name": "HadoopExploiter",
                        "options": {},
                        "supported_os": [
                            "LINUX",
                            "WINDOWS"
                        ]
                    },
                    {
                        "name": "Log4ShellExploiter",
                        "options": {},
                        "supported_os": [
                            "LINUX",
                            "WINDOWS"
                        ]
                    }
                ]
            }
        }
    }
"""


def build_default_agent_configuration() -> AgentConfiguration:
    schema = AgentConfigurationSchema()
    return schema.loads(DEFAULT_AGENT_CONFIGURATION_JSON)
