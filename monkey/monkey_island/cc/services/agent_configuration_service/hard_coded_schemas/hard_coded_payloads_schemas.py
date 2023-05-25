HARD_CODED_PAYLOADS_SCHEMAS = {
    "ransomware": {
        "type": "object",
        "properties": {
            "encryption": {
                "type": "object",
                "properties": {
                    "enabled": {
                        "title": " Encrypt files",
                        "type": "boolean",
                        "default": True,
                        "description": "Ransomware encryption will be simulated by flipping every "
                        "bit in the files contained within the target directories.",
                    },
                    "file_extension": {
                        "title": "File extension",
                        "type": "string",
                        "format": "valid-file-extension",
                        "default": ".m0nk3y",
                        "description": "The file extension that the Infection Monkey will use for "
                        "the encrypted file.",
                    },
                    "directories": {
                        "title": "Directories to encrypt",
                        "type": "object",
                        "properties": {
                            "linux_target_dir": {
                                "title": "Linux target directory",
                                "type": "string",
                                "format": "valid-ransomware-target-path-linux",
                                "default": "",
                                "description": "A path to a directory on Linux systems that "
                                "contains files you will allow Infection Monkey to encrypt. If no "
                                "directory is specified, no files will be encrypted.",
                            },
                            "windows_target_dir": {
                                "title": "Windows target directory",
                                "type": "string",
                                "format": "valid-ransomware-target-path-windows",
                                "default": "",
                                "description": "A path to a directory on Windows systems that "
                                "contains files you will allow Infection Monkey to encrypt. If no "
                                "directory is specified, no files will be encrypted.",
                            },
                        },
                    },
                    "algorithm": {
                        "title": "Encryption algorithm",
                        "type": "string",
                        "enum": ["BIT_FLIP", "AES256", "STEALTH_AES256"],
                        "default": "BIT_FLIP",
                        "description": "The algorithm to use for encrypting files. WARNING: The "
                        "BIT_FLIP algorithm is the only one that is considered to be safe for "
                        "use in production environments. The AES256 algorithm provides a more "
                        "realistic simulation and is intended for use in testing environments "
                        "only. The stealth AES256 algorithm does not rely on any "
                        "encryption-specific system calls or functions. This mechanism may slip "
                        "past detection tools that rely on specific system calls or CPU "
                        "instructions being used. Files encrypted with either AES256 algorithm "
                        "should be considered to be unrecoverable.",
                    },
                    "recursive": {
                        "title": "Recursive file discovery",
                        "type": "boolean",
                        "default": False,
                        "description": "Searches through the target directory recursively to find "
                        "all files in the directory and its subdirectories. WARNING: This option "
                        "is not safe for use in production environments.",
                    },
                },
            },
            "other_behaviors": {
                "title": "Other ransomware behavior",
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
}
