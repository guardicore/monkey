from common.configuration import AgentConfigurationSchema

flat_config = {
    "keep_tunnel_open_time": 30,
    "post_breach_actions": [
        {"name": "CommunicateAsBackdoorUser", "options": {}},
        {"name": "ModifyShellStartupFiles", "options": {}},
        {"name": "HiddenFiles", "options": {}},
        {"name": "TrapCommand", "options": {}},
        {"name": "ChangeSetuidSetgid", "options": {}},
        {"name": "ScheduleJobs", "options": {}},
        {"name": "Timestomping", "options": {}},
        {"name": "AccountDiscovery", "options": {}},
        {"name": "ProcessListCollection", "options": {}},
    ],
    "credential_collectors": [
        {"name": "MimikatzCollector", "options": {}},
        {"name": "SSHCollector", "options": {}},
    ],
    "payloads": [
        {
            "name": "ransomware",
            "options": {
                "encryption": {
                    "enabled": True,
                    "directories": {"linux_target_dir": "", "windows_target_dir": ""},
                },
                "other_behaviors": {"readme": True},
            },
        }
    ],
    "custom_pbas": {
        "linux_command": "",
        "linux_filename": "",
        "windows_command": "",
        "windows_filename": "",
    },
    "propagation": {
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
                    9600,
                ],
            },
            "icmp": {"timeout": 1000},
            "fingerprinters": [
                {"name": "elastic", "options": {}},
                {
                    "name": "http",
                    "options": {"http_ports": [80, 443, 7001, 8008, 8080, 8983, 9200, 9600]},
                },
                {"name": "mssql", "options": {}},
                {"name": "smb", "options": {}},
                {"name": "ssh", "options": {}},
            ],
            "targets": {
                "blocked_ips": [],
                "inaccessible_subnets": [],
                "local_network_scan": True,
                "subnets": [],
            },
        },
        "maximum_depth": 2,
        "exploitation": {
            "options": {"http_ports": [80, 443, 7001, 8008, 8080, 8983, 9200, 9600]},
            "brute_force": [
                {
                    "name": "MSSQLExploiter",
                    "options": {},
                },
                {
                    "name": "PowerShellExploiter",
                    "options": {},
                },
                {
                    "name": "SSHExploiter",
                    "options": {},
                },
                {
                    "name": "SmbExploiter",
                    "options": {"smb_download_timeout": 30},
                },
                {
                    "name": "WmiExploiter",
                    "options": {"smb_download_timeout": 30},
                },
            ],
            "vulnerability": [
                {
                    "name": "HadoopExploiter",
                    "options": {},
                },
                {
                    "name": "Log4ShellExploiter",
                    "options": {},
                },
            ],
        },
    },
}

DEFAULT_CONFIG = AgentConfigurationSchema().load(flat_config)
