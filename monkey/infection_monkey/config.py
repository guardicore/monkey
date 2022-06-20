import uuid
from abc import ABCMeta

GUID = str(uuid.getnode())

SENSITIVE_FIELDS = [
    "exploit_password_list",
    "exploit_user_list",
    "exploit_ssh_keys",
]
LOCAL_CONFIG_VARS = ["name", "id", "max_depth"]
HIDDEN_FIELD_REPLACEMENT_CONTENT = "hidden"


class Configuration(object):
    def from_kv(self, formatted_data):
        for key, value in list(formatted_data.items()):
            if key.startswith("_"):
                continue
            if key in LOCAL_CONFIG_VARS:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        if not self.max_depth:
            self.max_depth = self.depth

    @staticmethod
    def hide_sensitive_info(config_dict):
        for field in SENSITIVE_FIELDS:
            config_dict[field] = HIDDEN_FIELD_REPLACEMENT_CONTENT
        return config_dict

    def as_dict(self):
        result = {}
        for key in dir(Configuration):
            if key.startswith("_"):
                continue
            try:
                value = getattr(self, key)
            except AttributeError:
                continue

            val_type = type(value)

            if callable(value):
                continue

            if val_type in (type, ABCMeta):
                value = value.__name__
            elif val_type is tuple or val_type is list:
                if len(value) != 0 and type(value[0]) in (type, ABCMeta):
                    value = val_type([x.__name__ for x in value])

            result[key] = value

        return result

    ###########################
    # monkey config
    ###########################

    # depth of propagation
    depth = 0
    max_depth = None

    keep_tunnel_open_time = 30


WormConfiguration = Configuration()
