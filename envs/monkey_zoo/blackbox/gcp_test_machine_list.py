GCP_TEST_MACHINE_LIST = {
    "europe-west1-c": [
        "sshkeys-11",
        "sshkeys-12",
        "hadoop-2",
        "hadoop-3",
        "mssql-16",
        "mimikatz-14",
        "mimikatz-15",
        "tunneling-9",
        "tunneling-10",
        "tunneling-11",
        "tunneling-12",
        "tunneling-13",
        "zerologon-25",
    ],
    "europe-west1-b": [
        "powershell-3-44",
        "powershell-3-45",
        "powershell-3-46",
        "powershell-3-47",
        "powershell-3-48",
        "credentials-reuse-14",
        "credentials-reuse-15",
        "credentials-reuse-16",
        "log4j-logstash-55",
        "log4j-logstash-56",
        "log4j-solr-49",
        "log4j-solr-50",
        "log4j-tomcat-51",
        "log4j-tomcat-52",
        "snmp-20",
        "rdp-64",
        "rdp-65",
        "browser-credentials-66",
        "browser-credentials-67",
    ],
}

DEPTH_2_A = {
    "europe-west1-c": ["sshkeys-11", "sshkeys-12", "mimikatz-14", "mimikatz-15"],
    "europe-west1-b": [
        "powershell-3-46",
        "powershell-3-44",
        "rdp-64",
        "rdp-65",
    ],
}

DEPTH_1_A = {
    "europe-west1-c": ["hadoop-2", "hadoop-3", "mssql-16", "mimikatz-15"],
    "europe-west1-b": [
        "log4j-logstash-55",
        "log4j-logstash-56",
        "log4j-solr-49",
        "log4j-solr-50",
        "log4j-tomcat-51",
        "log4j-tomcat-52",
        "snmp-20",
        "browser-credentials-66",
        "browser-credentials-67",
    ],
}

DEPTH_3_A = {
    "europe-west1-d": [
        "tunneling-9",
        "tunneling-10",
        "tunneling-11",
    ],
    "europe-west1-b": [
        "powershell-3-45",
        "powershell-3-47",
        "powershell-3-48",
    ],
}

DEPTH_4_A = {
    "europe-west1-d": [
        "tunneling-9",
        "tunneling-10",
        "tunneling-12",
        "tunneling-13",
    ],
}

ZEROLOGON = {
    "europe-west1-c": [
        "zerologon-25",
    ],
}

CREDENTIALS_REUSE_SSH_KEY = {
    "europe-west1-b": [
        "credentials-reuse-14",
        "credentials-reuse-15",
        "credentials-reuse-16",
    ],
}

SMB_PTH = {"europe-west1-c": ["mimikatz-15"]}

GCP_SINGLE_TEST_LIST = {
    "test_depth_2_a": DEPTH_2_A,
    "test_depth_1_a": DEPTH_1_A,
    "test_depth_3_a": DEPTH_3_A,
    "test_depth_4_a": DEPTH_4_A,
    "test_zerologon_exploiter": ZEROLOGON,
    "test_credentials_reuse_ssh_key": CREDENTIALS_REUSE_SSH_KEY,
    "test_smb_pth": SMB_PTH,
}
