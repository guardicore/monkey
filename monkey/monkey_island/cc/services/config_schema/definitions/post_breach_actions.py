POST_BREACH_ACTIONS = {
    "title": "Post-Breach Actions",
    "description": "Runs scripts/commands on infected machines. These actions safely simulate what "
    "an adversary might do after breaching a new machine. Used in ATT&CK and Zero trust reports.",
    "type": "string",
    "anyOf": [
        {
            "type": "string",
            "enum": ["CommunicateAsBackdoorUser"],
            "title": "Communicate as Backdoor User",
            "safe": True,
            "info": "Attempts to create a new user, create HTTPS requests as that "
            "user and delete the user "
            "afterwards.",
            "attack_techniques": ["T1136"],
        },
        {
            "type": "string",
            "enum": ["ModifyShellStartupFiles"],
            "title": "Modify Shell Startup Files",
            "safe": True,
            "info": "Attempts to modify shell startup files, like ~/.profile, "
            "~/.bashrc, ~/.bash_profile "
            "in linux, and profile.ps1 in windows. Reverts modifications done"
            " afterwards.",
            "attack_techniques": ["T1156", "T1504"],
        },
        {
            "type": "string",
            "enum": ["HiddenFiles"],
            "title": "Hidden Files and Directories",
            "safe": True,
            "info": "Attempts to create a hidden file and remove it afterward.",
            "attack_techniques": ["T1158"],
        },
        {
            "type": "string",
            "enum": ["TrapCommand"],
            "title": "Trap Command",
            "safe": True,
            "info": "On Linux systems, attempts to trap a terminate signal in order "
            "to execute a command upon receiving that signal. Removes the trap afterwards.",
            "attack_techniques": ["T1154"],
        },
        {
            "type": "string",
            "enum": ["ChangeSetuidSetgid"],
            "title": "Setuid and Setgid",
            "safe": True,
            "info": "On Linux systems, attempts to set the setuid and setgid bits of "
            "a new file. "
            "Removes the file afterwards.",
            "attack_techniques": ["T1166"],
        },
        {
            "type": "string",
            "enum": ["ScheduleJobs"],
            "title": "Job Scheduling",
            "safe": True,
            "info": "Attempts to create a scheduled job on the system and remove it.",
            "attack_techniques": ["T1168", "T1053"],
        },
        {
            "type": "string",
            "enum": ["Timestomping"],
            "title": "Timestomping",
            "safe": True,
            "info": "Creates a temporary file and attempts to modify its time "
            "attributes. Removes the file afterwards.",
            "attack_techniques": ["T1099"],
        },
        {
            "type": "string",
            "enum": ["SignedScriptProxyExecution"],
            "title": "Signed Script Proxy Execution",
            "safe": False,
            "info": "On Windows systems, attempts to execute an arbitrary file "
            "with the help of a pre-existing signed script.",
            "attack_techniques": ["T1216"],
        },
        {
            "type": "string",
            "enum": ["AccountDiscovery"],
            "title": "Account Discovery",
            "safe": True,
            "info": "Attempts to get a listing of user accounts on the system.",
            "attack_techniques": ["T1087"],
        },
        {
            "type": "string",
            "enum": ["ClearCommandHistory"],
            "title": "Clear Command History",
            "safe": False,
            "info": "Attempts to clear the command history.",
            "attack_techniques": ["T1146"],
        },
        {
            "type": "string",
            "enum": ["ProcessListCollection"],
            "title": "Process List Collector",
            "safe": True,
            "info": "Collects a list of running processes on the machine.",
        },
    ],
}
