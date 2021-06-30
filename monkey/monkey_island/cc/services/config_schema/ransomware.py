RANSOMWARE = {
    "title": "Ransomware",
    "type": "object",
    "properties": {
        "encryption": {
            "title": "Encryption",
            "type": "object",
            "properties": {
                "enabled": {
                    "title": "Encrypt files",
                    "type": "boolean",
                    "default": True,
                    "description": "Ransomware encryption will be simulated by flipping every bit "
                    "in the files contained within the target directories.",
                },
                "directories": {
                    "title": "Directories to encrypt",
                    "type": "object",
                    "properties": {
                        "linux_target_dir": {
                            "title": "Linux target directory",
                            "type": "string",
                            "default": "",
                            "description": "A path to a directory on Linux systems that contains "
                            "files that you will allow Infection Monkey to encrypt. If no "
                            "directory is specified, no files will be encrypted.",
                        },
                        "windows_target_dir": {
                            "title": "Windows target directory",
                            "type": "string",
                            "default": "",
                            "description": "A path to a directory on Windows systems that contains "
                            "files that you will allow Infection Monkey to encrypt. If no "
                            "directory is specified, no files will be encrypted.",
                        },
                    },
                },
            },
        },
        "other_behaviors": {
            "title": "Other behavior",
            "type": "object",
            "properties": {
                "readme": {
                    "title": "Create a README.txt file",
                    "type": "boolean",
                    "default": True,
                    "description": "Creates a README.txt ransomware note on infected systems.",
                }
            },
        },
    },
}
