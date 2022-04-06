import os
import sys
import uuid
from abc import ABCMeta

GUID = str(uuid.getnode())

EXTERNAL_CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "monkey.bin")

SENSITIVE_FIELDS = [
    "exploit_password_list",
    "exploit_user_list",
    "exploit_ssh_keys",
    "aws_secret_access_key",
    "aws_session_token",
]
LOCAL_CONFIG_VARS = ["name", "id", "current_server", "max_depth"]
HIDDEN_FIELD_REPLACEMENT_CONTENT = "hidden"


class Configuration(object):
    def from_kv(self, formatted_data):
        unknown_items = []
        for key, value in list(formatted_data.items()):
            if key.startswith("_"):
                continue
            if key in LOCAL_CONFIG_VARS:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                unknown_items.append(key)
        if not self.max_depth:
            self.max_depth = self.depth
        return unknown_items

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
    # dropper config
    ###########################

    dropper_set_date = True
    dropper_date_reference_path_windows = r"%windir%\system32\kernel32.dll"
    dropper_date_reference_path_linux = "/bin/sh"

    ###########################
    # monkey config
    ###########################
    # sets whether or not the monkey is alive. if false will stop scanning and exploiting
    should_stop = False

    # depth of propagation
    depth = 2
    max_depth = None
    current_server = ""

    # Configuration servers to try to connect to, in this order.
    command_servers = []

    keep_tunnel_open_time = 30

    ###########################
    # testing configuration
    ###########################
    export_monkey_telems = False


WormConfiguration = Configuration()
