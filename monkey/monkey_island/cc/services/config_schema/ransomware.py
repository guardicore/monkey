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
                    "description": "Selected files will be encrypted using bitflip to simulate "
                    "ransomware. Enter target directories below.",
                },
                "directories": {
                    "title": "Directories to encrypt",
                    "type": "object",
                    "properties": {
                        "linux_dir": {
                            "title": "Linux encryptable directory",
                            "type": "string",
                            "default": "",
                            "description": "Files in the specified directory will be encrypted "
                            "using bitflip to simulate ransomware.",
                        },
                        "windows_dir": {
                            "title": "Windows encryptable directory",
                            "type": "string",
                            "default": "",
                            "description": "Files in the specified directory will be encrypted "
                            "using bitflip to simulate ransomware.",
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
