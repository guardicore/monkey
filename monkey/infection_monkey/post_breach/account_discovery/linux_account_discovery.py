def get_linux_commands_to_discover_accounts():
    return [
        "echo \'Discovered the following user accounts:\'; ",
        "cut -d: -f1,3 /etc/passwd | ",
        "egrep ':[0-9]{4}$' | ",
        "cut -d: -f1"
    ]
