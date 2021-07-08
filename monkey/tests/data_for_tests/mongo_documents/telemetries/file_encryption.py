from mongomock import ObjectId

ENCRYPTED = {
    "_id": ObjectId("60e541c37a6cdf66484ba517"),
    "monkey_guid": "211375648895908",
    "telem_category": "file_encryption",
    "data": {
        "files": [
            {"path": "infection_monkey.py", "success": True, "error": ""},
            {"path": "monkey_island.py", "success": True, "error": ""},
            {"path": "__init__.py", "success": True, "error": ""},
        ]
    },
    "timestamp": "2021-07-07T08:55:15.830Z",
    "command_control_channel": {"src": "192.168.56.1", "dst": "192.168.56.1:5000"},
}

ENCRYPTED_2 = {
    "_id": ObjectId("60e54fee7a6cdf66484ba559"),
    "monkey_guid": "211375648895908",
    "telem_category": "file_encryption",
    "data": {
        "files": [
            {"path": "infection_monkey.py", "success": True, "error": ""},
            {"path": "monkey_island.py", "success": True, "error": ""},
            {"path": "__init__.py", "success": True, "error": ""},
        ]
    },
    "timestamp": "2021-07-07T09:55:42.311Z",
    "command_control_channel": {"src": "192.168.56.1", "dst": "192.168.56.1:5000"},
}

ENCRYPTION_ERROR = {
    "_id": ObjectId("60e56f167a6cdf66484ba5aa"),
    "monkey_guid": "211375648895908",
    "telem_category": "file_encryption",
    "data": {
        "files": [
            {
                "path": "C:\\w\\Dump\\README.txt",
                "success": False,
                "error": "[WinError 183] Cannot create a file when that "
                "file already exists: 'C:\\\\w\\\\Dump\\\\README.txt'"
                " -> 'C:\\\\w\\\\Dump\\\\README.txt.m0nk3y'",
            }
        ]
    },
    "timestamp": "2021-07-07T12:08:38.058Z",
    "command_control_channel": {"src": "192.168.56.1", "dst": "192.168.56.1:5000"},
}

ENCRYPTION_ONE_FILE = {
    "_id": ObjectId("60e56f1b7a6cdf66484ba5c0"),
    "monkey_guid": "91758264576",
    "telem_category": "file_encryption",
    "data": {"files": [{"path": "C:\\w\\Dump\\README.txt", "success": True, "error": ""}]},
    "timestamp": "2021-07-07T12:08:43.421Z",
    "command_control_channel": {"src": "172.25.33.145", "dst": "172.25.32.1:5000"},
}
