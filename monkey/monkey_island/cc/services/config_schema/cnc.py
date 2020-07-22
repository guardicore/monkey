CNC = {
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
}
