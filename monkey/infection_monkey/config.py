import hashlib
import os
import json
import sys
import types
import uuid
from abc import ABCMeta
from itertools import product
import importlib

__author__ = 'itamar'

GUID = str(uuid.getnode())

EXTERNAL_CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'monkey.bin')

SENSITIVE_FIELDS = ["exploit_password_list", "exploit_user_list"]
HIDDEN_FIELD_REPLACEMENT_CONTENT = "hidden"


class Configuration(object):
    def from_kv(self, formatted_data):
        # now we won't work at <2.7 for sure
        network_import = importlib.import_module('infection_monkey.network')
        exploit_import = importlib.import_module('infection_monkey.exploit')

        unknown_items = []
        for key, value in formatted_data.items():
            if key.startswith('_'):
                continue
            if key in ["name", "id", "current_server"]:
                continue
            if self._depth_from_commandline and key == "depth":
                continue
            # handle in cases
            if key == 'finger_classes':
                class_objects = [getattr(network_import, val) for val in value]
                setattr(self, key, class_objects)
            elif key == 'exploiter_classes':
                class_objects = [getattr(exploit_import, val) for val in value]
                setattr(self, key, class_objects)
            else:
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    unknown_items.append(key)
        return unknown_items

    def from_json(self, json_data):
        """
        Gets a json data object, parses it and applies it to the configuration
        :param json_data:
        :return:
        """
        formatted_data = json.loads(json_data)
        result = self.from_kv(formatted_data)
        return result

    @staticmethod
    def hide_sensitive_info(config_dict):
        for field in SENSITIVE_FIELDS:
            config_dict[field] = HIDDEN_FIELD_REPLACEMENT_CONTENT
        return config_dict

    def as_dict(self):
        result = {}
        for key in dir(Configuration):
            if key.startswith('_'):
                continue
            try:
                value = getattr(self, key)
            except AttributeError:
                continue

            val_type = type(value)

            if val_type is types.FunctionType or val_type is types.MethodType:
                continue

            if val_type in (type, ABCMeta):
                value = value.__name__
            elif val_type is tuple or val_type is list:
                if len(value) != 0 and type(value[0]) in (type, ABCMeta):
                    value = val_type([x.__name__ for x in value])

            result[key] = value

        return result

    # Used to keep track of our depth if manually specified
    _depth_from_commandline = False

    ###########################
    # logging config
    ###########################

    use_file_logging = True
    dropper_log_path_windows = '%temp%\\~df1562.tmp'
    dropper_log_path_linux = '/tmp/user-1562'
    monkey_log_path_windows = '%temp%\\~df1563.tmp'
    monkey_log_path_linux = '/tmp/user-1563'
    send_log_to_server = True

    ###########################
    # dropper config
    ###########################

    dropper_try_move_first = True
    dropper_set_date = True
    dropper_date_reference_path_windows = r"%windir%\system32\kernel32.dll"
    dropper_date_reference_path_linux = '/bin/sh'
    dropper_target_path_win_32 = r"C:\Windows\temp\monkey32.exe"
    dropper_target_path_win_64 = r"C:\Windows\temp\monkey64.exe"
    dropper_target_path_linux = '/tmp/monkey'

    ###########################
    # Kill file
    ###########################
    kill_file_path_windows = '%windir%\\monkey.not'
    kill_file_path_linux = '/var/run/monkey.not'

    ###########################
    # monkey config
    ###########################
    # sets whether or not the monkey is alive. if false will stop scanning and exploiting
    alive = True

    # sets whether or not to self delete the monkey executable when stopped
    self_delete_in_cleanup = False

    # string of the mutex name for single instance
    singleton_mutex_name = "{2384ec59-0df8-4ab9-918c-843740924a28}"

    # how long to wait between scan iterations
    timeout_between_iterations = 100

    # how many scan iterations to perform on each run
    max_iterations = 1

    finger_classes = []
    exploiter_classes = []

    # how many victims to look for in a single scan iteration
    victims_max_find = 30

    # how many victims to exploit before stopping
    victims_max_exploit = 7

    # depth of propagation
    depth = 2
    current_server = ""

    # Configuration servers to try to connect to, in this order.
    command_servers = [
        "192.0.2.0:5000"
    ]

    # sets whether or not to locally save the running configuration after finishing
    serialize_config = False

    # sets whether or not to retry failed hosts on next scan
    retry_failed_explotation = True

    # addresses of internet servers to ping and check if the monkey has internet acccess.
    internet_services = ["updates.infectionmonkey.com", "www.google.com"]

    keep_tunnel_open_time = 60

    # Monkey files directory name
    monkey_dir_name = 'monkey_dir'

    ###########################
    # scanners config
    ###########################

    # Auto detect and scan local subnets
    local_network_scan = True

    subnet_scan_list = []
    inaccessible_subnets = []

    blocked_ips = []

    # TCP Scanner
    HTTP_PORTS = [80, 8080, 443,
                  8008,  # HTTP alternate
                  7001  # Oracle Weblogic default server port
                  ]
    tcp_target_ports = [22,
                        2222,
                        445,
                        135,
                        3389,
                        80,
                        8080,
                        443,
                        8008,
                        3306,
                        9200]
    tcp_target_ports.extend(HTTP_PORTS)
    tcp_scan_timeout = 3000  # 3000 Milliseconds
    tcp_scan_interval = 0
    tcp_scan_get_banner = True

    # Ping Scanner
    ping_scan_timeout = 1000

    ###########################
    # exploiters config
    ###########################

    should_exploit = True
    skip_exploit_if_file_exist = False

    ms08_067_exploit_attempts = 5
    user_to_add = "Monkey_IUSER_SUPPORT"
    remote_user_pass = "Password1!"

    # rdp exploiter
    rdp_use_vbs_download = True

    # User and password dictionaries for exploits.

    def get_exploit_user_password_pairs(self):
        """
        Returns all combinations of the configurations users and passwords
        :return:
        """
        return product(self.exploit_user_list, self.exploit_password_list)

    def get_exploit_user_ssh_key_pairs(self):
        """
        :return: All combinations of the configurations users and ssh pairs
        """
        return product(self.exploit_user_list, self.exploit_ssh_keys)

    def get_exploit_user_password_or_hash_product(self):
        """
        Returns all combinations of the configurations users and passwords or lm/ntlm hashes
        :return:
        """
        cred_list = []
        for cred in product(self.exploit_user_list, self.exploit_password_list, [''], ['']):
            cred_list.append(cred)
        for cred in product(self.exploit_user_list, [''], [''], self.exploit_ntlm_hash_list):
            cred_list.append(cred)
        for cred in product(self.exploit_user_list, [''], self.exploit_lm_hash_list, ['']):
            cred_list.append(cred)
        return cred_list

    exploit_user_list = ['Administrator', 'root', 'user']
    exploit_password_list = ["Password1!", "1234", "password", "12345678"]
    exploit_lm_hash_list = []
    exploit_ntlm_hash_list = []
    exploit_ssh_keys = []

    # smb/wmi exploiter
    smb_download_timeout = 300  # timeout in seconds
    smb_service_name = "InfectionMonkey"

    # Timeout (in seconds) for sambacry's trigger to yield results.
    sambacry_trigger_timeout = 5
    # Folder paths to guess share lies inside.
    sambacry_folder_paths_to_guess = ['/', '/mnt', '/tmp', '/storage', '/export', '/share', '/shares', '/home']
    # Shares to not check if they're writable.
    sambacry_shares_not_to_check = ["IPC$", "print$"]

    # system info collection
    collect_system_info = True
    should_use_mimikatz = True

    ###########################
    # systeminfo config
    ###########################

    extract_azure_creds = True

    post_breach_actions = []
    custom_PBA_linux_cmd = ""
    custom_PBA_windows_cmd = ""
    PBA_linux_filename = None
    PBA_windows_filename = None

    @staticmethod
    def hash_sensitive_data(sensitive_data):
        """
        Hash sensitive data (e.g. passwords). Used so the log won't contain sensitive data plain-text, as the log is
        saved on client machines plain-text.

        :param sensitive_data: the data to hash.
        :return: the hashed data.
        """
        password_hashed = hashlib.sha512(sensitive_data).hexdigest()
        return password_hashed


WormConfiguration = Configuration()
