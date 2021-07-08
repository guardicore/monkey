from mongomock import ObjectId

EDGE_EXPLOITED = {
    "_id": ObjectId("60e541c07a6cdf66484ba504"),
    "_cls": "Edge.EdgeService",
    "src_node_id": ObjectId("60e541aab6732b49f4c564ea"),
    "dst_node_id": ObjectId("60e541c6b6732b49f4c56622"),
    "scans": [
        {
            "timestamp": "2021-07-07T08:55:12.866Z",
            "data": {
                "os": {"type": "windows"},
                "services": {"tcp-445": {"display_name": "SMB", "port": 445}},
                "icmp": True,
                "monkey_exe": None,
                "default_tunnel": None,
                "default_server": None,
            },
        }
    ],
    "exploits": [
        {
            "result": True,
            "exploiter": "SmbExploiter",
            "info": {
                "display_name": "SMB",
                "started": "2021-07-07T08:55:12.944Z",
                "finished": "2021-07-07T08:55:14.376Z",
                "vulnerable_urls": [],
                "vulnerable_ports": ["139 or 445", "139 or 445"],
                "executed_cmds": [],
            },
            "attempts": [
                {
                    "result": False,
                    "user": "Administrator",
                    "password": "LydBuBjDAe/igLGS2FyeKL1zLoTt0r+CkaPH1v5/Vr7HmzcbBPW562Io+MQlrMey",
                    "lm_hash": "",
                    "ntlm_hash": "",
                    "ssh_key": "",
                },
                {
                    "result": True,
                    "user": "user",
                    "password": "Evzzovf6QLOPUja78/nP6XgiNXH5bB1MrXqPBYmBgeQDOcBhJPUE32+8968zDlHy",
                    "lm_hash": "",
                    "ntlm_hash": "",
                    "ssh_key": "",
                },
            ],
            "timestamp": "2021-07-07T08:55:14.420Z",
        },
        {
            "result": True,
            "exploiter": "SmbExploiter",
            "info": {
                "display_name": "SMB",
                "started": "2021-07-07T12:08:35.168Z",
                "finished": "2021-07-07T12:08:36.612Z",
                "vulnerable_urls": [],
                "vulnerable_ports": ["139 or 445", "139 or 445"],
                "executed_cmds": [],
            },
            "attempts": [
                {
                    "result": False,
                    "user": "Administrator",
                    "password": "B4o8ujKpBfKyjCvb7c5bHr7a8CzwfOJi+i228WGv4/9OZZaEsKjps/5Zg1aHSEun",
                    "lm_hash": "",
                    "ntlm_hash": "",
                    "ssh_key": "",
                },
                {
                    "result": True,
                    "user": "user",
                    "password": "Evzzovf6QLOPUja78/nP6XgiNXH5bB1MrXqPBYmBgeQDOcBhJPUE32+8968zDlHy",
                    "lm_hash": "",
                    "ntlm_hash": "",
                    "ssh_key": "",
                },
            ],
            "timestamp": "2021-07-07T12:08:36.650Z",
        },
    ],
    "tunnel": False,
    "exploited": True,
    "src_label": "MonkeyIsland - test-pc-2 : 192.168.56.1",
    "dst_label": "WinDev2010Eval : 172.25.33.145",
    "domain_name": "",
    "ip_address": "172.25.33.145",
}

EDGE_SCANNED = {
    "_id": ObjectId("60e6b24dc10b80a409c048a3"),
    "_cls": "Edge.EdgeService",
    "src_node_id": ObjectId("60e541aab6732b49f4c564ea"),
    "dst_node_id": ObjectId("60e6b24dc10b80a409c048a2"),
    "scans": [
        {
            "timestamp": "2021-07-08T11:07:41.407Z",
            "data": {
                "os": {"type": "linux", "version": "Ubuntu-4ubuntu0.3"},
                "services": {
                    "tcp-22": {
                        "display_name": "SSH",
                        "port": 22,
                        "banner": "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n",
                        "name": "ssh",
                    }
                },
                "icmp": True,
                "monkey_exe": None,
                "default_tunnel": None,
                "default_server": None,
            },
        }
    ],
    "exploits": [],
    "tunnel": False,
    "exploited": False,
    "src_label": "MonkeyIsland - test-pc-2 : 192.168.56.1",
    "dst_label": "Ubuntu-4ubuntu0.3 : 172.24.125.179",
    "domain_name": "",
    "ip_address": "172.24.125.179",
}
