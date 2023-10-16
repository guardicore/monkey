HARD_CODED_FINGERPRINTER_SCHEMAS = {
    "smb": {"type": "object", "properties": {}},
    "ssh": {"type": "object", "properties": {}},
    "http": {
        "type": "object",
        "properties": {
            "http_ports": {
                "title": "HTTP Ports",
                "type": "array",
                "items": {"type": "integer", "minimum": 0, "maximum": 65535},
                "default": [80, 8080, 443, 8008, 7001, 8983, 9600],
                "description": "List of HTTP ports the fingerprinter will scan",
            }
        },
    },
    "mssql": {"type": "object", "properties": {}},
}
