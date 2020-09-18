from common.data.system_info_collectors_names import (AWS_COLLECTOR,
                                                      AZURE_CRED_COLLECTOR,
                                                      ENVIRONMENT_COLLECTOR,
                                                      HOSTNAME_COLLECTOR,
                                                      MIMIKATZ_COLLECTOR,
                                                      PROCESS_LIST_COLLECTOR)

MONKEY = {
    "title": "Monkey",
    "type": "object",
    "properties": {
        "post_breach": {
            "title": "Post breach",
            "type": "object",
            "properties": {
                "custom_PBA_linux_cmd": {
                    "title": "Linux post breach command",
                    "type": "string",
                    "default": "",
                    "description": "Linux command to be executed after breaching."
                },
                "PBA_linux_file": {
                    "title": "Linux post breach file",
                    "type": "string",
                    "format": "data-url",
                    "description": "File to be executed after breaching. "
                                   "If you want custom execution behavior, "
                                   "specify it in 'Linux post breach command' field. "
                                   "Reference your file by filename."
                },
                "custom_PBA_windows_cmd": {
                    "title": "Windows post breach command",
                    "type": "string",
                    "default": "",
                    "description": "Windows command to be executed after breaching."
                },
                "PBA_windows_file": {
                    "title": "Windows post breach file",
                    "type": "string",
                    "format": "data-url",
                    "description": "File to be executed after breaching. "
                                   "If you want custom execution behavior, "
                                   "specify it in 'Windows post breach command' field. "
                                   "Reference your file by filename."
                },
                "PBA_windows_filename": {
                    "title": "Windows PBA filename",
                    "type": "string",
                    "default": ""
                },
                "PBA_linux_filename": {
                    "title": "Linux PBA filename",
                    "type": "string",
                    "default": ""
                },
                "post_breach_actions": {
                    "title": "Post breach actions",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "$ref": "#/definitions/post_breach_actions"
                    },
                    "default": [
                        "BackdoorUser",
                        "CommunicateAsNewUser",
                        "ModifyShellStartupFiles",
                        "HiddenFiles",
                        "TrapCommand",
                        "ChangeSetuidSetgid",
                        "ScheduleJobs",
                        "Timestomping",
                        "AccountDiscovery"
                    ]
                },
            }
        },
        "system_info": {
            "title": "System info",
            "type": "object",
            "properties": {
                "system_info_collector_classes": {
                    "title": "System info collectors",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "$ref": "#/definitions/system_info_collector_classes"
                    },
                    "default": [
                        ENVIRONMENT_COLLECTOR,
                        AWS_COLLECTOR,
                        HOSTNAME_COLLECTOR,
                        PROCESS_LIST_COLLECTOR,
                        MIMIKATZ_COLLECTOR,
                        AZURE_CRED_COLLECTOR
                    ]
                },
            }
        },
        "persistent_scanning": {
            "title": "Persistent scanning",
            "type": "object",
            "properties": {
                "max_iterations": {
                    "title": "Max iterations",
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "description": "Determines how many iterations of the monkey's full lifecycle should occur "
                                   "(how many times to do the scan)"
                },
                "timeout_between_iterations": {
                    "title": "Wait time between iterations",
                    "type": "integer",
                    "default": 100,
                    "minimum": 0,
                    "description":
                        "Determines for how long (in seconds) should the monkey wait before starting another scan"
                },
                "retry_failed_explotation": {
                    "title": "Retry failed exploitation",
                    "type": "boolean",
                    "default": True,
                    "description":
                        "Determines whether the monkey should retry exploiting machines"
                        " it didn't successfully exploit on previous scans"
                }
            }
        }
    }
}
