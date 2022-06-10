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
                    "default": 30,
                    "description": "Time to keep tunnel open before going down after last exploit "
                    "(in seconds)",
                },
            },
        },
        "monkey": {
            "title": "Monkey",
            "type": "object",
            "properties": {
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
                            "default": [80, 8080, 443, 8008, 7001, 9200, 8983, 9600],
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
                                5985,
                                5986,
                            ],
                            "description": "List of TCP ports the monkey will check whether "
                            "they're open",
                        },
                        "tcp_scan_timeout": {
                            "title": "TCP scan timeout",
                            "type": "integer",
                            "default": 3000,
                            "description": "Maximum time (in milliseconds) "
                            "to wait for TCP response",
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
