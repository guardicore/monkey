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
                    "description": "List of IPs that the Monkey will not scan.",
                    "info": "The Monkey scans its subnet if \"Local network scan\" is ticked. "
                            "Additionally the monkey scans machines according to \"Scan target list\"."
                },
                "local_network_scan": {
                    "title": "Local network scan",
                    "type": "boolean",
                    "default": True,
                    "description": "Determines whether the Monkey will scan the local subnets of machines it runs on, "
                                   "in addition to the IPs that are configured manually in the \"Scan target list\"."
                },
                "depth": {
                    "title": "Scan depth",
                    "type": "integer",
                    "minimum": 1,
                    "default": 2,
                    "description":
                        "Amount of hops allowed for the Monkey to spread from the Island server. \n"
                        + WARNING_SIGN
                        + " Note that setting this value too high may result in the Monkey propagating too far, "
                          "if the \"Local network scan\" is enabled."
                },
                "subnet_scan_list": {
                    "title": "Scan target list",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string",
                        "format": IP_RANGE
                    },
                    "default": [
                    ],
                    "description":
                        "List of targets the Monkey will try to scan. Targets can be IPs, subnets or hosts."
                        " Examples:\n"
                        "\tTarget a specific IP: \"192.168.0.1\"\n"
                        "\tTarget a subnet using a network range: \"192.168.0.5-192.168.0.20\"\n"
                        "\tTarget a subnet using an IP mask: \"192.168.0.5/24\"\n"
                        "\tTarget a specific host: \"printer.example\""
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
                        "Test for network segmentation by providing a list of network segments "
                        "that should NOT be accessible to each other.\n\n"
                        "For example, if you configured the following three segments: "
                        "\"10.0.0.0/24\", \"11.0.0.2/32\", and \"12.2.3.0/24\", "
                        "a Monkey running on 10.0.0.5 will try to access machines in the following subnets: "
                        "11.0.0.2/32, 12.2.3.0/24. An alert on successful cross-segment connections "
                        "will be shown in the reports. \n\n"
                        "Network segments can be IPs, subnets or hosts. Examples:\n"
                        "\tDefine a single-IP segment: \"192.168.0.1\"\n"
                        "\tDefine a segment using a network range: \"192.168.0.5-192.168.0.20\"\n"
                        "\tDefine a segment using an subnet IP mask: \"192.168.0.5/24\"\n"
                        "\tDefine a single-host segment: \"printer.example\""
                }
            }
        }
    }
}
