from common.data.validation_formats import IP, IP_RANGE
from monkey_island.cc.services.utils.typographic_symbols import WARNING_SIGN

BASIC_NETWORK = {
    "title": "Network",
    "type": "object",
    "properties": {
        "scope": {
            "title": "Scope",
            "type": "object",
            "properties": {
                "blocked_ips": {
                    "title": "Blocked IPs",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string",
                        "format": IP,
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
                    "minimum": 1,
                    "default": 2,
                    "description":
                        "Amount of hops allowed for the monkey to spread from the island. "
                        + WARNING_SIGN
                        + " Note that setting this value too high may result in the monkey propagating too far"
                },
                "subnet_scan_list": {
                    "title": "Scan IP/subnet list",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string",
                        "format": IP_RANGE
                    },
                    "default": [
                    ],
                    "description":
                        "List of IPs/subnets/hosts the monkey should scan."
                        " Examples: \"192.168.0.1\", \"192.168.0.5-192.168.0.20\", \"192.168.0.5/24\","
                        " \"printer.example\""
                }
            }
        },
        "network_analysis": {
            "title": "Network Analysis",
            "type": "object",
            "properties": {
                "inaccessible_subnets": {
                    "title": "Network segmentation testing",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string",
                        "format": IP_RANGE
                    },
                    "default": [
                    ],
                    "description":
                        "Test for network segmentation by providing a list of"
                        " subnets that should NOT be accessible to each other."
                        " For example, given the following configuration:"
                        " '10.0.0.0/24, 11.0.0.2/32, 12.2.3.0/24'"
                        " a Monkey running on 10.0.0.5 will try to access machines in the following"
                        " subnets: 11.0.0.2/32, 12.2.3.0/24."
                        " An alert on successful connections will be shown in the report"
                        " Additional subnet formats include: 13.0.0.1, 13.0.0.1-13.0.0.5"
                }
            }
        }
    }
}
