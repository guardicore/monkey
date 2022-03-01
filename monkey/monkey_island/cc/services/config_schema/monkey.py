from common.common_consts.credential_collector_names import MIMIKATZ_COLLECTOR, SSH_COLLECTOR

MONKEY = {
    "title": "Monkey",
    "type": "object",
    "properties": {
        "post_breach": {
            "title": "Post breach",
            "type": "object",
            "properties": {
                "custom_PBA_linux_cmd": {
                    "title": "Linux post-breach command",
                    "type": "string",
                    "default": "",
                    "description": "Command to be executed after breaching. "
                    "Use this field to run custom commands or execute uploaded "
                    "files on exploited machines.\nExample: "
                    '"chmod +x ./my_script.sh; ./my_script.sh ; rm ./my_script.sh"',
                },
                "PBA_linux_file": {
                    "title": "Linux post-breach file",
                    "type": "string",
                    "format": "data-url",
                    "description": "File to be uploaded after breaching. "
                    "Use the 'Linux post-breach command' field to "
                    "change permissions, run, or delete the file. "
                    "Reference your file by filename.",
                },
                "custom_PBA_windows_cmd": {
                    "title": "Windows post-breach command",
                    "type": "string",
                    "default": "",
                    "description": "Command to be executed after breaching. "
                    "Use this field to run custom commands or execute uploaded "
                    "files on exploited machines.\nExample: "
                    '"my_script.bat & del my_script.bat"',
                },
                "PBA_windows_file": {
                    "title": "Windows post-breach file",
                    "type": "string",
                    "format": "data-url",
                    "description": "File to be uploaded after breaching. "
                    "Use the 'Windows post-breach command' field to "
                    "change permissions, run, or delete the file. "
                    "Reference your file by filename.",
                },
                "PBA_windows_filename": {
                    "title": "Windows PBA filename",
                    "type": "string",
                    "default": "",
                },
                "PBA_linux_filename": {
                    "title": "Linux PBA filename",
                    "type": "string",
                    "default": "",
                },
                "post_breach_actions": {
                    "title": "Post breach actions",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"$ref": "#/definitions/post_breach_actions"},
                    "default": [
                        "CommunicateAsBackdoorUser",
                        "ModifyShellStartupFiles",
                        "HiddenFiles",
                        "TrapCommand",
                        "ChangeSetuidSetgid",
                        "ScheduleJobs",
                        "Timestomping",
                        "AccountDiscovery",
                        "ProcessListCollection",
                    ],
                },
            },
        },
        "credential_collectors": {
            "title": "Credential collection",
            "type": "object",
            "properties": {
                "credential_collector_classes": {
                    "title": "Credential collectors",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"$ref": "#/definitions/credential_collector_classes"},
                    "default": [
                        MIMIKATZ_COLLECTOR,
                        SSH_COLLECTOR,
                    ],
                },
            },
        },
    },
}
