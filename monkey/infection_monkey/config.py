import uuid

GUID = str(uuid.getnode())

SENSITIVE_FIELDS = [
    "exploit_password_list",
    "exploit_user_list",
    "exploit_ssh_keys",
]
LOCAL_CONFIG_VARS = ["name", "id", "max_depth"]
HIDDEN_FIELD_REPLACEMENT_CONTENT = "hidden"
