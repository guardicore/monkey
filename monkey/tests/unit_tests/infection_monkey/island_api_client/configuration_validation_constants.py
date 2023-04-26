SCHEMA = {
    "title": "AgentConfiguration",
    "type": "object",
    "properties": {
        "keep_tunnel_open_time": {
            "title": "Keep tunnel open time",
            "description": "Time to keep \ntunnel open before going down after last exploit (in seconds)",
            "default": 30,
            "minimum": 0,
            "type": "number",
        },
        "credentials_collectors": {
            "title": "Credentials collectors",
            "type": "object",
            "items": {"$ref": "#/definitions/CredentialsCollectorsConfiguration"},
        },
        "payloads": {
            "title": "Payloads",
            "type": "object",
        },
        "propagation": {
            "title": "Propagation",
            "allOf": [{"$ref": "#/definitions/PropagationConfiguration"}],
        },
    },
    "required": ["credentials_collectors", "payloads", "propagation"],
    "additionalProperties": False,
    "definitions": {
        "PluginConfiguration": {
            "title": "PluginConfiguration",
            "description": 'A configuration for plugins\n\nAttributes:\n    :param name: Name of the plugin\n                 Example: "ransomware"\n    :param options: Any other information/configuration fields relevant to the plugin\n                    Example: {\n                        "encryption": {\n                            "enabled": True,\n                            "directories": {\n                                "linux_target_dir": "~/this_dir",\n                                "windows_target_dir": "C:   hat_dir"\n                            },\n                        },\n                        "other_behaviors": {\n                            "readme": True\n                        },\n                    }',
            "type": "object",
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "options": {"title": "Options", "type": "object"},
            },
            "required": ["name", "options"],
            "additionalProperties": False,
        },
        "CredentialsCollectorsConfiguration": {
            "title": "CredentialsCollectorsConfiguration",
            "description": "",
            "type": "object",
            "properties": {
                "credentials_collectors": {
                    "SSHCollector": {},
                    "MockCollector": {
                        "type": "object",
                        "title": "MockCollector",
                        "safe": True,
                        "description": "Collects something cool!",
                        "link": "https://techdocs.akamai.com/infection-monkey",
                        "properties": {},
                    },
                }
            },
            "additionalProperties": False,
        },
        "TCPScanConfiguration": {
            "title": "TCPScanConfiguration",
            "description": "A configuration for TCP scanning\n\nAttributes:\n    :param timeout: Maximum time in seconds to wait for a response from the target\n    :param ports: Ports to scan",
            "type": "object",
            "properties": {
                "timeout": {
                    "title": "TCP scan timeout",
                    "description": "Maximum time to wait for TCP response in seconds",
                    "default": 3.0,
                    "exclusiveMinimum": 0,
                    "type": "number",
                },
                "ports": {
                    "title": "TCP target ports",
                    "description": "List of TCP ports the monkey will check whether they're open",
                    "default": [
                        22,
                        2222,
                        445,
                        135,
                        389,
                        80,
                        8080,
                        443,
                        8008,
                        3306,
                        7001,
                        8088,
                        5885,
                        5986,
                    ],
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0, "maximum": 65535},
                },
            },
            "additionalProperties": False,
        },
        "ICMPScanConfiguration": {
            "title": "ICMPScanConfiguration",
            "description": "A configuration for ICMP scanning\n\nAttributes:\n    :param timeout: Maximum time in seconds to wait for a response from the target",
            "type": "object",
            "properties": {
                "timeout": {
                    "title": "Ping scan timeout",
                    "description": "Maximum time to wait for ping response in seconds",
                    "default": 1.0,
                    "exclusiveMinimum": 0,
                    "type": "number",
                }
            },
            "additionalProperties": False,
        },
        "ScanTargetConfiguration": {
            "title": "ScanTargetConfiguration",
            "description": 'Configuration of network targets to scan and exploit\n\nAttributes:\n    :param blocked_ips: IP\\\'s that won\\\'t be scanned\n                        Example: ("1.1.1.1", "2.2.2.2")\n    :param inaccessible_subnets: Subnet ranges that shouldn\\\'t be accessible for the agent\n                                 Example: ("1.1.1.1", "2.2.2.2/24", "myserver")\n    :param scan_my_networks: If true the Agent will scan networks it belongs to\n     in addition to the provided subnet ranges\n    :param subnets: Subnet ranges to scan\n                    Example: ("192.168.1.1-192.168.2.255", "3.3.3.3", "2.2.2.2/24",\n                              "myHostname")',
            "type": "object",
            "properties": {
                "blocked_ips": {
                    "title": "Blocked IPs",
                    "description": "List of IPs that the monkey will not scan.",
                    "default": [],
                    "type": "array",
                    "items": {"type": "string"},
                },
                "inaccessible_subnets": {
                    "title": "Network segmentation testing",
                    "description": 'Test for network segmentation by providing a list of network segments that should not be accessible to each other.\n\n For example, if you configured the following three segments: "10.0.0.0/24", "11.0.0.2/32" and "12.2.3.0/24",a Monkey running on 10.0.0.5 will try to access machines in the following subnets: 11.0.0.2/32, 12.2.3.0/24. An alert on successful cross-segment connections will be shown in the reports. \n\nNetwork segments can be IPs, subnets or hosts. Examples:\n\tDefine a single-IP segment: "192.168.0.1"\n\tDefine a segment using a network range: "192.168.0.5-192.168.0.20"\n\tDefine a segment using an subnet IP mask: "192.168.0.5/24"\n\tDefine a single-host segment: "printer.example"\n\n Note that the networks configured in this section will be scanned using ping sweep.',
                    "default": [],
                    "type": "array",
                    "items": {"type": "string"},
                },
                "scan_my_networks": {
                    "title": "Scan Agent's networks",
                    "default": False,
                    "type": "boolean",
                },
                "subnets": {
                    "title": "Scan target list",
                    "description": 'List of targets the Monkey will try to scan. Targets can be IPs, subnets or hosts. Examples:\n\tTarget a specific IP: "192.168.0.1"\n\tTarget a subnet using a network range: "192.168.0.5-192.168.0.20"\n\tTarget a subnet using an IP mask: "192.168.0.5/24"\n\tTarget a specific host: "printer.example"',
                    "default": [],
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "additionalProperties": False,
        },
        "NetworkScanConfiguration": {
            "title": "NetworkScanConfiguration",
            "description": "A configuration for network scanning\n\nAttributes:\n    :param tcp: Configuration for TCP scanning\n    :param icmp: Configuration for ICMP scanning\n    :param fingerprinters: Configuration for fingerprinters to run\n    :param targets: Configuration for targets to scan",
            "type": "object",
            "properties": {
                "tcp": {
                    "title": "TCP scanner",
                    "allOf": [{"$ref": "#/definitions/TCPScanConfiguration"}],
                },
                "icmp": {
                    "title": "Ping scanner",
                    "allOf": [{"$ref": "#/definitions/ICMPScanConfiguration"}],
                },
                "fingerprinters": {
                    "title": "Fingerprinters",
                    "description": "Fingerprint modules collect info about external services",
                    "type": "array",
                    "items": {"$ref": "#/definitions/PluginConfiguration"},
                },
                "targets": {
                    "title": "Network",
                    "description": 'If "Scan Agent\\\'s networks" is checked, the Monkey scans for machines on each of the network interfaces of the machine it is running on.\nAdditionally, the Monkey scans machines according to "Scan target list" and skips machines in "Blocked IPs".',
                    "allOf": [{"$ref": "#/definitions/ScanTargetConfiguration"}],
                },
            },
            "required": ["tcp", "icmp", "fingerprinters", "targets"],
            "additionalProperties": False,
        },
        "ExploitationOptionsConfiguration": {
            "title": "ExploitationOptionsConfiguration",
            "description": "A configuration for exploitation options\n\nAttributes:\n    :param http_ports: HTTP ports to exploit",
            "type": "object",
            "properties": {
                "http_ports": {
                    "title": "HTTP Ports",
                    "description": "List of ports the monkey will check if are being used for HTTP",
                    "default": [80, 8080, 443, 8008, 7001, 8983, 9600],
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0, "maximum": 65535},
                }
            },
            "additionalProperties": False,
        },
        "ExploitationConfiguration": {
            "title": "ExploitationConfiguration",
            "description": "A configuration for exploitation\n\nAttributes:\n    :param options: Exploitation options shared by all exploiters\n    :param exploiters: Configuration enabled exploiters",
            "type": "object",
            "properties": {
                "options": {
                    "title": "Exploiters Options",
                    "allOf": [{"$ref": "#/definitions/ExploitationOptionsConfiguration"}],
                },
                "exploiters": {
                    "title": "Enabled exploiters",
                    "type": "object",
                    "properties": {
                        "ZerologonExploiter": {
                            "type": "object",
                            "title": "Zerologon Exploiter",
                            "safe": False,
                            "description": "Exploits a privilege escalation vulnerability (CVE-2020-1472) in a Windows server domain controller (DC) by using the Netlogon Remote Protocol (MS-NRPC). This exploiter changes the password of a Windows server DC account, steals credentials, and then attempts to restore the original DC password. The victim DC will be unable to communicate with other DCs until the original password has been restored. If Infection Monkey fails to restore the password automatically, you'll have to do it manually. For more information, see the documentation.",
                            "link": "https://techdocs.akamai.com/infection-monkey/docs/zerologon/",
                            "properties": {},
                        },
                        "Log4ShellExploiter": {
                            "type": "object",
                            "title": "Log4Shell Exploiter",
                            "safe": True,
                            "description": "Exploits a software vulnerability (CVE-2021-44228) in Apache Log4j, a Java logging framework. Exploitation is attempted on the following services - Apache Solr, Apache Tomcat, Logstash.",
                            "link": "https://techdocs.akamai.com/infection-monkey/docs/log4shell/",
                            "properties": {},
                        },
                        "PowerShellExploiter": {
                            "type": "object",
                            "title": "PowerShell Remoting Exploiter",
                            "description": "Exploits PowerShell remote execution setups. PowerShell Remoting uses Windows Remote Management (WinRM) to allow users to run PowerShell commands on remote computers.",
                            "safe": True,
                            "link": "https://techdocs.akamai.com/infection-monkey/docs/powershell",
                            "properties": {},
                        },
                        "WmiExploiter": {
                            "type": "object",
                            "title": "WMI Exploiter",
                            "safe": True,
                            "description": "Brute forces WMI (Windows Management Instrumentation) using credentials provided by user and hashes gathered by mimikatz.",
                            "link": "https://techdocs.akamai.com/infection-monkey/docs/wmiexec/",
                            "properties": {
                                "smb_download_timeout": {
                                    "title": "SMB download timeout",
                                    "description": "Maximum time allowd for uploading the Agent binary to the target",
                                    "type": "number",
                                    "default": 30,
                                    "minimum": 0,
                                    "maximum": 100,
                                }
                            },
                        },
                        "MSSQLExploiter": {
                            "type": "object",
                            "title": "MSSQL Exploiter",
                            "safe": True,
                            "description": "Tries to brute force into MsSQL server and uses insecure configuration to execute commands on server.",
                            "link": "https://techdocs.akamai.com/infection-monkey/docs/mssql/",
                            "properties": {},
                        },
                        "SSHExploiter": {
                            "type": "object",
                            "title": "SSH Exploiter",
                            "safe": True,
                            "description": "Brute forces using credentials provided by user and SSH keys gathered from systems.",
                            "link": "https://techdocs.akamai.com/infection-monkey/docs/sshexec/",
                            "properties": {},
                        },
                        "Mock1": {
                            "title": "Mock1 exploiter",
                            "description": "Configuration settings for Mock1 exploiter.",
                            "type": "object",
                            "required": ["exploitation_success_rate", "propagation_success_rate"],
                            "properties": {
                                "exploitation_success_rate": {
                                    "title": "Exploitation success rate",
                                    "description": "The rate of successful exploitation in percentage",
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 100,
                                    "default": 50,
                                },
                                "propagation_success_rate": {
                                    "title": "Propagation success rate",
                                    "description": "The rate of successful propagation in percentage",
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 100,
                                    "default": 50,
                                },
                                "list_of_strings": {
                                    "title": "List of random strings",
                                    "description": "A list of random strings for testing",
                                    "type": "array",
                                    "uniqueItems": True,
                                    "items": {"type": "string"},
                                    "default": [],
                                },
                                "ssh_key": {
                                    "title": "SSH key pair",
                                    "description": "An SSH key pair field for testing",
                                    "type": "object",
                                    "properties": {
                                        "public_key": {"title": "Public key", "type": "string"},
                                        "private_key": {"title": "Private key", "type": "string"},
                                    },
                                },
                                "random_boolean": {
                                    "title": "Random boolean",
                                    "description": "A random boolean field for testing",
                                    "type": "boolean",
                                    "default": True,
                                },
                                "sleep_duration": {
                                    "title": "Sleep duration",
                                    "description": "Duration in seconds for which the plugin should sleep",
                                    "type": "number",
                                    "default": 0,
                                },
                            },
                        },
                    },
                    "additionalProperties": False,
                },
            },
            "required": ["options", "exploiters"],
            "additionalProperties": False,
        },
        "PropagationConfiguration": {
            "title": "PropagationConfiguration",
            "description": "A configuration for propagation\n\nAttributes:\n    :param maximum_depth: Maximum number of hops allowed to spread from the machine where\n                          the attack started i.e. how far to propagate in the network from the\n                          first machine\n    :param network_scan: Configuration for network scanning\n    :param exploitation: Configuration for exploitation",
            "type": "object",
            "properties": {
                "maximum_depth": {
                    "title": "Maximum scan depth",
                    "description": 'Amount of hops allowed for the monkey to spread from the Island server. \n  Note that setting this value too high may result in the Monkey propagating too far, if "Scan Agent\\\'s networks" is enabled.\nSetting this to 0 will disable all scanning and exploitation.',
                    "default": 2,
                    "minimum": 0,
                    "type": "integer",
                },
                "network_scan": {
                    "title": "Network analysis",
                    "allOf": [{"$ref": "#/definitions/NetworkScanConfiguration"}],
                },
                "exploitation": {
                    "title": "Exploiters",
                    "allOf": [{"$ref": "#/definitions/ExploitationConfiguration"}],
                },
            },
            "required": ["network_scan", "exploitation"],
            "additionalProperties": False,
        },
    },
}
