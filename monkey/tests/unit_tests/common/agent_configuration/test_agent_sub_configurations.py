from common.agent_configuration import TCPScanConfiguration

expected_tcp_schema = {
    "type": "object",
    "properties": {
        "timeout": {
            "title": "TCP scan timeout",
            "description": "Maximum time to wait for TCP response",
            "default": 3.0,
            "exclusiveMinimum": 0,
            "type": "number",
        },
        "ports": {
            "title": "TCP target ports",
            "description": "List of TCP ports the monkey will check whether they're open",
            "default": [22, 2222, 445, 135, 389, 80, 8080, 443, 8008, 3306, 7001, 8088, 5885, 5986],
            "type": "array",
            "items": {"type": "integer", "minimum": 0, "maximum": 65535},
        },
    },
    "additionalProperties": False,
}


def test_sub_config_to_json_schema():
    tcp_schema = TCPScanConfiguration.schema()
    # Title and description is irrelevant in this case, because in full schema the parent
    # schema will define these
    del tcp_schema["title"]
    del tcp_schema["description"]

    assert tcp_schema == expected_tcp_schema
