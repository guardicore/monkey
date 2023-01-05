PLUGIN_NAME = "bond"
PLUGIN_OPTIONS = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
PLUGIN_CONFIGURATION = {"name": PLUGIN_NAME, "options": PLUGIN_OPTIONS}

BLOCKED_IPS = ["10.0.0.1", "192.168.1.1"]
INACCESSIBLE_SUBNETS = ["172.0.0.0/24", "172.2.2.0/24", "192.168.56.0/24"]
SCAN_MY_NETWORKS = True
SUBNETS = ["10.0.0.2", "10.0.0.2/16"]
SCAN_TARGET_CONFIGURATION = {
    "blocked_ips": BLOCKED_IPS,
    "inaccessible_subnets": INACCESSIBLE_SUBNETS,
    "scan_my_networks": SCAN_MY_NETWORKS,
    "subnets": SUBNETS,
}

TIMEOUT = 2.525
ICMP_CONFIGURATION = {"timeout": TIMEOUT}

PORTS = [0, 8080, 443]
TCP_SCAN_CONFIGURATION = {"timeout": TIMEOUT, "ports": PORTS}

FINGERPRINTERS = [{"name": "mssql", "options": {}}]
NETWORK_SCAN_CONFIGURATION = {
    "tcp": TCP_SCAN_CONFIGURATION,
    "icmp": ICMP_CONFIGURATION,
    "fingerprinters": FINGERPRINTERS,
    "targets": SCAN_TARGET_CONFIGURATION,
}

EXPLOITERS = [
    {"name": "ex1", "options": {}},
    {
        "name": "ex2",
        "options": {"smb_download_timeout": 10},
    },
    {
        "name": "ex3",
        "options": {"smb_download_timeout": 10},
    },
]
EXPLOITATION_CONFIGURATION = {
    "options": {"http_ports": PORTS},
    "exploiters": EXPLOITERS,
}

PROPAGATION_CONFIGURATION = {
    "maximum_depth": 5,
    "network_scan": NETWORK_SCAN_CONFIGURATION,
    "exploitation": EXPLOITATION_CONFIGURATION,
}

AGENT_CONFIGURATION = {
    "keep_tunnel_open_time": 30,
    "credential_collectors": [PLUGIN_CONFIGURATION],
    "payloads": [PLUGIN_CONFIGURATION],
    "propagation": PROPAGATION_CONFIGURATION,
}
