NETWORK = {
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
                        7001,
                        8088
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
