from common.common_consts.validation_formats import (
    VALID_RANSOMWARE_TARGET_PATH_LINUX,
    VALID_RANSOMWARE_TARGET_PATH_WINDOWS,
)

RANSOMWARE = {
    "title": "Ransomware",
    "type": "object",
    "description": "This page allows you to configure the Infection Monkey to execute a ransomware "
    "simulation. The Infection Monkey is capable of simulating a ransomware attack on your network "
    "using a set of configurable behaviors. A number of precautions have been taken to ensure that "
    "this ransomware simulation is safe for production environments.\n\nFor more information about "
    "configuring the ransomware simulation, see "
    '<a href="https://guardicore.com/infectionmonkey/docs/usage/use-cases/ransomware-simulation" '
    'target="_blank"> the documentation</a>.',
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
                "readme_note": {
                    "title": "",
                    "type": "object",
                    "description": "Note: A README.txt will be left in the specified target "
                    "directory.",
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
