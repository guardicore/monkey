from mongomock import ObjectId

MONKEY_AT_ISLAND = {
    "_id": ObjectId("60e541aab6732b49f4c564ea"),
    "guid": "211375648895908",
    "config": {},
    "creds": [],
    "dead": True,
    "description": "Windows test-pc-2 10",
    "hostname": "test-pc-2",
    "internet_access": True,
    "ip_addresses": [
        "192.168.56.1",
        "172.17.192.1",
        "172.25.32.1",
        "192.168.43.1",
        "192.168.10.1",
        "192.168.0.102",
    ],
    "keepalive": "2021-07-07T12:08:13.164Z",
    "modifytime": "2021-07-07T12:10:13.340Z",
    "parent": [
        ["211375648895908", None],
        ["211375648895908", None],
        ["211375648895908", None],
        ["211375648895908", None],
    ],
    "ttl_ref": ObjectId("60e56f757a6cdf66484ba5cc"),
    "command_control_channel": {"src": "192.168.56.1", "dst": "192.168.56.1:5000"},
    "pba_results": [],
}

MONKEY_AT_VICTIM = {
    "_id": ObjectId("60e541c6b6732b49f4c56622"),
    "guid": "91758264576",
    "config": {},
    "creds": [],
    "dead": False,
    "description": "Windows WinDev2010Eval 10 10.0.19041 AMD64 Intel64 Family 6 Model 165 "
    "Stepping 2, GenuineIntel",
    "hostname": "WinDev2010Eval",
    "internet_access": True,
    "ip_addresses": ["172.25.33.145"],
    "keepalive": "2021-07-07T12:08:41.200Z",
    "modifytime": "2021-07-07T12:08:47.144Z",
    "parent": [["211375648895908", "SmbExploiter"], ["211375648895908", None]],
    "ttl_ref": ObjectId("60e56f1f7a6cdf66484ba5c5"),
    "command_control_channel": {"src": "172.25.33.145", "dst": "172.25.32.1:5000"},
    "pba_results": [],
}
