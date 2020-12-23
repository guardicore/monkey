BASIC = {
    "title": "Exploits",
    "type": "object",
    "primary": True,
    "properties": {
        "exploiters": {
            "title": "Exploiters",
            "type": "object",
            "description": "Choose which exploiters the Monkey will attempt.",
            "properties": {
                "exploiter_classes": {
                    "title": "Exploiters",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "$ref": "#/definitions/exploiter_classes"
                    },
                    "default": [
                        "SmbExploiter",
                        "WmiExploiter",
                        "SSHExploiter",
                        "ShellShockExploiter",
                        "SambaCryExploiter",
                        "ElasticGroovyExploiter",
                        "Struts2Exploiter",
                        "WebLogicExploiter",
                        "HadoopExploiter",
                        "VSFTPDExploiter",
                        "MSSQLExploiter",
                        "DrupalExploiter",
                        "ZerologonExploiter"
                    ]
                }
            }
        },
        "credentials": {
            "title": "Credentials",
            "type": "object",
            "properties": {
                "exploit_user_list": {
                    "title": "Exploit user list",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string"
                    },
                    "default": [
                        "Administrator",
                        "root",
                        "user"
                    ],
                    "description": "List of user names that will be used by exploiters that need credentials, like "
                                   "SSH brute-forcing."
                },
                "exploit_password_list": {
                    "title": "Exploit password list",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string"
                    },
                    "default": [
                        "root",
                        "123456",
                        "password",
                        "123456789",
                        "qwerty",
                        "111111",
                        "iloveyou"
                    ],
                    "description": "List of passwords that will be used by exploiters that need credentials, like "
                                   "SSH brute-forcing."
                }
            }
        }
    }
}
