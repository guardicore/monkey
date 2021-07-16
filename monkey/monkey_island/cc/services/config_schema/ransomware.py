from common.common_consts.validation_formats import (
    VALID_RANSOMWARE_TARGET_PATH_LINUX,
    VALID_RANSOMWARE_TARGET_PATH_WINDOWS,
)

RANSOMWARE = {
    "title": "Ransomware",
    "type": "object",
    "properties": {
        "encryption": {
            "title": "Simulation",
            "type": "object",
            "description": "To simulate ransomware encryption, you'll need to provide Infection "
            "Monkey with files that it can safely encrypt. On each machine where you would like "
            "the ransomware simulation to run, create a directory and put some files in it."
            "\n\nProvide the path to the directory that was created on each machine.",
            "properties": {
                "enabled": {
                    "title": "Encrypt files",
                    "type": "boolean",
                    "default": True,
                    "description": "Ransomware encryption will be simulated by flipping every bit "
                    "in the files contained within the target directories.",
                },
                "info_box": {
                    "info": "No files will be encrypted if a directory is not specified or doesn't "
                    "exist on a victim machine.",
                },
                "directories": {
                    "title": "Directories to encrypt",
                    "type": "object",
                    "properties": {
                        "linux_target_dir": {
                            "title": "Linux target directory",
                            "type": "string",
                            "format": VALID_RANSOMWARE_TARGET_PATH_LINUX,
                            "default": "",
                            "description": "A path to a directory on Linux systems that contains "
                            "files that you will allow Infection Monkey to encrypt. If no "
                            "directory is specified, no files will be encrypted.",
                        },
                        "windows_target_dir": {
                            "title": "Windows target directory",
                            "type": "string",
                            "format": VALID_RANSOMWARE_TARGET_PATH_WINDOWS,
                            "default": "",
                            "description": "A path to a directory on Windows systems that contains "
                            "files that you will allow Infection Monkey to encrypt. If no "
                            "directory is specified, no files will be encrypted.",
                        },
                    },
                },
                "text_box": {
                    "text": "Note: A README.txt will be left in the specified target " "directory.",
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
