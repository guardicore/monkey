PLUGIN_NAME = "bond"
PLUGIN_OPTIONS = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
PLUGIN_CONFIGURATION = {"name": PLUGIN_NAME, "options": PLUGIN_OPTIONS}

LINUX_COMMAND = "a"
LINUX_FILENAME = "b"
WINDOWS_COMMAND = "c"
WINDOWS_FILENAME = "d"
CUSTOM_PBA_CONFIGURATION = {
    "linux_command": LINUX_COMMAND,
    "linux_filename": LINUX_FILENAME,
    "windows_command": WINDOWS_COMMAND,
    "windows_filename": WINDOWS_FILENAME,
}

BLOCKED_IPS = ["10.0.0.1", "192.168.1.1"]
INACCESSIBLE_SUBNETS = ["172.0.0.0/24", "172.2.2.0/24", "192.168.56.0/24"]
SCAN_LOCAL_INTERFACES = True
SUBNETS = ["10.0.0.2", "10.0.0.2/16"]
SCAN_TARGET_CONFIGURATION = {
    "blocked_ips": BLOCKED_IPS,
    "inaccessible_subnets": INACCESSIBLE_SUBNETS,
    "scan_local_interfaces": SCAN_LOCAL_INTERFACES,
    "subnets": SUBNETS,
}

TIMEOUT = 2.525
ICMP_CONFIGURATION = {"timeout": TIMEOUT}

PORTS = [8080, 443]
TCP_SCAN_CONFIGURATION = {"timeout": TIMEOUT, "ports": PORTS}

FINGERPRINTERS = [{"name": "mssql", "options": {}}]
NETWORK_SCAN_CONFIGURATION = {
    "tcp": TCP_SCAN_CONFIGURATION,
    "icmp": ICMP_CONFIGURATION,
    "fingerprinters": FINGERPRINTERS,
    "targets": SCAN_TARGET_CONFIGURATION,
}

BRUTE_FORCE = [
    {"name": "ex1", "options": {}},
    {
        "name": "ex2",
        "options": {"smb_download_timeout": 10},
    },
]
VULNERABILITY = [
    {
        "name": "ex3",
        "options": {"smb_download_timeout": 10},
    },
]
EXPLOITATION_CONFIGURATION = {
    "options": {"http_ports": PORTS},
    "brute_force": BRUTE_FORCE,
    "vulnerability": VULNERABILITY,
}

PROPAGATION_CONFIGURATION = {
    "maximum_depth": 5,
    "network_scan": NETWORK_SCAN_CONFIGURATION,
    "exploitation": EXPLOITATION_CONFIGURATION,
}

AGENT_CONFIGURATION = {
    "keep_tunnel_open_time": 30,
    "custom_pbas": CUSTOM_PBA_CONFIGURATION,
    "post_breach_actions": [PLUGIN_CONFIGURATION],
    "credential_collectors": [PLUGIN_CONFIGURATION],
    "payloads": [PLUGIN_CONFIGURATION],
    "propagation": PROPAGATION_CONFIGURATION,
}
